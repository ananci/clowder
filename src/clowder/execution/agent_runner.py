import json
from abc import ABC, abstractmethod
from typing import Type, TypeVar, Any
from pydantic import BaseModel

# We use a TypeVar so your IDE knows exactly what type of Pydantic model is being returned!
T = TypeVar('T', bound=BaseModel)

class BaseRunner(ABC):
    """
    The core contract for all execution engines. 
    The Orchestrator only interacts with this interface, ensuring we are never locked into one provider.
    """
    @abstractmethod
    def process_item(self, item_data: Any, system_prompt: str, response_schema: Type[T]) -> T:
        pass


class GeminiRunner(BaseRunner):
    """Cloud execution engine using Google's flagship models."""
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        from google import genai
        from google.genai import types # pyright: ignore[reportUnusedImport]
        self.client = genai.Client()
        self.model_name = model_name

    def process_item(self, item_data: Any, system_prompt: str, response_schema: Type[T]) -> T:
        if isinstance(item_data, dict):
            raw_text = json.dumps(item_data, indent=2)
        else:
            raw_text = str(item_data)
            
        user_prompt = f"Please process the following data:\n\n{raw_text}"

        config = types.GenerateContentConfig( # pyright: ignore[reportUndefinedVariable, reportUnknownMemberType] # type: ignore
            system_instruction=system_prompt,
            response_mime_type="application/json",
            response_schema=response_schema,
            temperature=0.0
        )

        response = self.client.models.generate_content( # pyright: ignore[reportUnknownMemberType]
            model=self.model_name,
            contents=user_prompt,
            config=config # pyright: ignore[reportUnknownArgumentType]
        )

        if not response.text:
            raise ValueError("LLM returned an empty response.")
            
        return response_schema.model_validate_json(response.text)


class LocalDevRunner(BaseRunner):
    """
    Local execution engine for rapid framework development.
    Currently stubbed to return mock data instantly. Later, we can 
    swap this with actual KerasNLP or vLLM inference code.
    """
    def __init__(self, model_name: str):
        self.model_name = model_name

    def process_item(self, item_data: Any, system_prompt: str, response_schema: Type[T]) -> T:
        from rich.console import Console
        Console().print(f"[dim]  🤖 (LocalDevRunner faking LLM processing for {response_schema.__name__})[/dim]")
        
        # Dynamically build mock data that perfectly matches the requested Pydantic schema
        mock_data = {}
        for field_name, field_info in response_schema.model_fields.items():
            if field_info.annotation == str: mock_data[field_name] = "local_mock_string"
            elif field_info.annotation == int: mock_data[field_name] = 42
            elif field_info.annotation == bool: mock_data[field_name] = True
            elif field_info.annotation == list[str]: mock_data[field_name] = ["mock_1", "mock_2"]
            else: mock_data[field_name] = None
            
        # Returns a valid instance of the schema without invoking a real LLM
        return response_schema.model_construct(**mock_data) # type: ignore


def get_runner(engine: str, model_name: str) -> BaseRunner:
    """Factory function to route to the correct execution engine."""
    if engine == "cloud":
        return GeminiRunner(model_name)
    elif engine in ["local_server", "embedded"]:
        # For now, local runs use the instant dev stub
        return LocalDevRunner(model_name)
    else:
        raise ValueError(f"Unknown engine: {engine}")