# The Typer/Rich CLI interface with streaming progress bars

import typer
from rich.console import Console

# Initialize the Typer app and Rich console
app = typer.Typer(help="Clowder: A MapReduce-style LLM Orchestrator")
console = Console()

@app.command()
def hello(name: str = "World"):
    """
    A simple Hello World command to test the Typer CLI.
    """
    # Rich uses simple bracket tags for formatting, like HTML!
    console.print(f"[bold green]Hello, {name}! Welcome to Clowder.[/bold green] 🐾")

@app.command()
def run(pipeline_path: str):
    """
    (Placeholder) Will eventually run a pipeline YAML file.
    """
    console.print(f"[bold blue]Preparing to run pipeline from:[/bold blue] {pipeline_path}")

# This is the modern entry point!
if __name__ == "__main__":
    app()