# Forces LLM JSON output into strict Pydantic typesimport importlib
import importlib
import sys
from pathlib import Path
from typing import Type
from pydantic import BaseModel
from rich.console import Console

console = Console()

def load_schema(schema_string: str) -> Type[BaseModel]:
    """
    Takes a string like 'schemas.EmailSummary' and dynamically imports 
    the actual Python class from the user's directory.
    """
    try:
        module_name, class_name = schema_string.split('.')
    except ValueError:
        console.print(f"[bold red]Error:[/bold red] Invalid schema format '{schema_string}'. Expected format: 'module.ClassName'")
        raise SystemExit(1)

    # Ensure the user's current directory is in the Python path so we can find their files
    cwd = str(Path.cwd())
    if cwd not in sys.path:
        sys.path.insert(0, cwd)

    try:
        # Dynamically import the module (e.g., schemas.py)
        module = importlib.import_module(module_name)
        # Grab the class (e.g., EmailSummary)
        schema_class = getattr(module, class_name)
        return schema_class
    except (ImportError, AttributeError) as e:
        console.print(f"[bold red]Error:[/bold red] Could not load schema '{schema_string}'.\nMake sure the file exists and the class name is correct.\nDetails: {e}")
        raise SystemExit(1)