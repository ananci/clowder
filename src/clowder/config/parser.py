# Reads the YAML and Markdown files

import yaml
from pathlib import Path
from pydantic import ValidationError
from rich.console import Console

from clowder.config.models import PipelineConfig

console = Console()

def load_pipeline(file_path: str | Path) -> PipelineConfig:
    """Reads a YAML file and validates it against the PipelineConfig schema."""
    path = Path(file_path)
    
    if not path.exists():
        console.print(f"[bold red]Error:[/bold red] Pipeline file not found at '{path}'")
        raise SystemExit(1)

    try:
        with open(path, "r", encoding="utf-8") as f:
            raw_data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        console.print(f"[bold red]YAML Parse Error:[/bold red]\n{e}")
        raise SystemExit(1)

    try:
        # Pydantic does all the heavy lifting here
        # It takes the raw dictionary and forces it into our strict schema.
        pipeline = PipelineConfig(**raw_data)
        return pipeline
    except ValidationError as e:
        console.print("[bold red]Pipeline Validation Failed![/bold red] Your YAML is missing fields or has the wrong data types.")
        console.print(e)
        raise SystemExit(1)