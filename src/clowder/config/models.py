# Pydantic models representing the Pipeline, Stages, etc.

from typing import Literal, Optional, List
from pydantic import BaseModel, Field # pyright: ignore[reportUnusedImport]

class GlobalSettings(BaseModel):
    engine: Literal["cloud", "local_server", "embedded"] = "cloud"
    model: str
    endpoint: Optional[str] = None

class StageConfig(BaseModel):
    name: str
    type: Literal["single", "fan_out", "reduce"]
    agent_prompt: str
    # We will use this later to dynamically import the user's custom schema
    output_schema: str 
    
class TriggerConfig(BaseModel):
    source: str

class PipelineConfig(BaseModel):
    name: str
    global_settings: GlobalSettings
    trigger: TriggerConfig
    stages: List[StageConfig]
    sink: str