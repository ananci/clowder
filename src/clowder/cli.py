import typer
from pathlib import Path
from rich.console import Console

# Import our parser
from clowder.config.parser import load_pipeline

# Initialize the Typer app and Rich console
app = typer.Typer(help="Clowder: A MapReduce-style LLM Orchestrator")
console = Console()

@app.command()
def run(pipeline_path: Path = typer.Argument(..., help="Path to the pipeline.yaml file")):
    """
    Runs a Clowder pipeline defined in a YAML file.
    """
    console.print(f"[bold blue]Loading pipeline from:[/bold blue] {pipeline_path}")
    
    # 1. Pass the path directly to our parser
    pipeline = load_pipeline(pipeline_path)
    
    # 2. Print out the successfully parsed Pydantic data!
    console.print(f"[bold green]Successfully parsed pipeline:[/bold green] {pipeline.name}")
    console.print(f"Engine requested: [yellow]{pipeline.global_settings.engine}[/yellow] using model [yellow]{pipeline.global_settings.model}[/yellow]")
    console.print(f"Found [magenta]{len(pipeline.stages)}[/magenta] stages to execute.")

if __name__ == "__main__":
    app()