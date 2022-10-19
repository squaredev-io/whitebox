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


@app.command("serve_simulator")
def serve_app_simulator(
    env: Optional[Environment] = Environment.dev,
    host: str = "0.0.0.0",
    port: int = 8001,
):
    typer.echo(f"\nRunning API | Environment: {env} 🚀 \n")
    os.system(
        f"ENV='{env}' uvicorn src.simulator:simulator_app --reload --host {host} --port {port}"
    )


@app.command("serve_cron")
def serve_cron(
    env: Optional[Environment] = Environment.dev,
    host: str = "0.0.0.0",
    port: int = 8002,
):
    typer.echo(f"\nRunning API | Environment: {env} 🚀 \n")
    os.system(
        f"ENV='{env}' uvicorn src.cron:cron_app --reload --host {host} --port {port}"
    )


@app.command("seed")
def seed(env: Optional[Environment] = Environment.dev):
    typer.echo(f"\nRunning Seed | Environment: {env} 🚀 \n")
    os.system('export PYTHONPATH="${PYTHONPATH}:/src"')
    os.system(f"ENV='{env}' python3 src/utils/seed.py")


@app.command()
def test():
    os.system(f"ENV=test pytest -s")


try:
    from eralchemy import render_er

    @app.command("generate_diagram")
    def generate_er_diagram():
        typer.echo(f"\nGenerate ER diagram 🚀 \n")
        render_er(Base, "src/assets/er/er_diagram.er")
        render_er(Base, "src/assets/er/er_diagram.dot")
        render_er(Base, "src/assets/er/er_diagram.png")

except ImportError as e:
    pass


if __name__ == "__main__":
    app()
