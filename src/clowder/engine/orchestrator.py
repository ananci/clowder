# The main DAG traversal loop

from rich.console import Console
from typing import List, Dict, Union
from clowder.config.models import PipelineConfig

console = Console()

class Orchestrator:
    def __init__(self, pipeline: PipelineConfig):
        self.pipeline = pipeline

    def run(self):
        console.print(f"\n[bold magenta]🚀 Starting Execution: {self.pipeline.name}[/bold magenta]")
        
        # 1. The Trigger Phase
        source = self.pipeline.trigger.source
        console.print(f"[cyan]📥 Loading data from:[/cyan] {source}")
        # MOCK: Pretend we loaded a JSON file with 5 items. The actual type will be more specific.
        mock_data: List[Dict[str, Union[int, str]]] = [{"id": 1, "text": "Sample email text"}] * 5 
        
        # 2. The Stages Phase
        current_data = mock_data
        for i, stage in enumerate(self.pipeline.stages, 1):
            console.print(f"\n[bold yellow]⚙️  Executing Stage {i}: {stage.name} ({stage.type})[/bold yellow]")
            console.print(f"  ↳ Agent Prompt: {stage.agent_prompt}")
            console.print(f"  ↳ Output Schema: {stage.output_schema}")
            
            # In the future, this is where we will hand off to fan_out.py
            console.print(f"  ↳ [dim]Simulating processing of {len(current_data)} items...[/dim]")
            
        # 3. The Sink Phase
        sink = self.pipeline.sink
        console.print(f"\n[cyan]📤 Writing results to:[/cyan] {sink}")
        console.print("[bold green]✅ Pipeline Complete![/bold green]")