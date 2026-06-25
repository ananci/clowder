import json
from pathlib import Path
from rich.console import Console

from clowder.config.models import PipelineConfig
from clowder.execution.agent_runner import get_runner
from clowder.execution.schema_parser import load_schema

console = Console()

class Orchestrator:
    def __init__(self, pipeline: PipelineConfig):
        self.pipeline = pipeline
        self.runner = get_runner(
            engine=self.pipeline.global_settings.engine,
            model_name=self.pipeline.global_settings.model
        )

    def run(self):
        console.print(f"\n[bold magenta]🚀 Starting Execution: {self.pipeline.name}[/bold magenta]")
        
        # 1. The Trigger Phase (Real File I/O)
        source = self.pipeline.trigger.source.replace("file://", "")
        console.print(f"[cyan]📥 Loading data from:[/cyan] {source}")
        
        try:
            with open(source, 'r', encoding='utf-8') as f:
                current_data = json.load(f)
        except Exception as e:
            console.print(f"[bold red]Failed to load trigger data:[/bold red] {e}")
            raise SystemExit(1)
        
        # 2. The Stages Phase
        for i, stage in enumerate(self.pipeline.stages, 1):
            console.print(f"\n[bold yellow]⚙️  Executing Stage {i}: {stage.name} ({stage.type})[/bold yellow]")
            
            # Dynamically load the exact Pydantic schema requested in the YAML!
            stage_schema = load_schema(stage.output_schema)
            
            results = []
            for item in current_data: # type: ignore
                result = self.runner.process_item(
                    item_data=item,
                    system_prompt=stage.agent_prompt,
                    response_schema=stage_schema
                )
                results.append(result) # type: ignore
            
            console.print(f"  ↳ [green]Successfully processed {len(results)} items![/green]") # type: ignore
            # Pass the processed Pydantic models forward as the data for the next stage (if any)
            current_data = results
                
        # 3. The Sink Phase (Real File I/O)
        sink = self.pipeline.sink.replace("file://", "")
        console.print(f"\n[cyan]📤 Writing results to:[/cyan] {sink}")
        
        # Convert our Pydantic objects back to standard dictionaries for saving
        final_output = [item.model_dump() for item in current_data] # type: ignore
        
        # Make sure the output directory exists
        Path(sink).parent.mkdir(parents=True, exist_ok=True)
        with open(sink, 'w', encoding='utf-8') as f:
            json.dump(final_output, f, indent=2)
            
        console.print("[bold green]✅ Pipeline Complete![/bold green]")