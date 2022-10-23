#! ./.venv/bin/python

import os
from typing import Optional
from enum import Enum
from src.models.Base import Base

try:
    import typer
except ImportError as e:
    os.system("pip install typer")
    import typer


app = typer.Typer()


class Environment(str, Enum):
    dev = "dev"
    test = "test"
    staging = "staging"
    production = "production"


@app.command()
def venv(venv: Optional[str] = "venv"):
    typer.echo("\nCreating virtual environment 🍇")
    os.system(f"python -m venv .{venv}")
    command = typer.style(
        f"`source .{venv}/bin/activate`", fg=typer.colors.GREEN, bold=True
    )
    typer.echo(f"\nActivate with: {command}. Happy coding 😁 \n")


@app.command()
def install():
    typer.echo("\nInstalling packages 🚀")
    os.system("pip install -r src/requirements.txt")
    typer.echo(f"\nPackages installed. Have fun 😁 \n")


@app.command()
def serve(
    env: Optional[Environment] = Environment.dev,
    host: str = "0.0.0.0",
    port: int = 8000,
):
    typer.echo(f"\nRunning API | Environment: {env} 🚀 \n")
    os.system(f"ENV='{env}' uvicorn src.main:app --reload --host {host} --port {port}")


@app.command()
def test():
    os.system(f"ENV=test pytest -s")


if __name__ == "__main__":
    app()
