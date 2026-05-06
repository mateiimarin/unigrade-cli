"""Command-line interface for unigrade."""

import typer

app = typer.Typer()


@app.callback()
def main_callback():
    pass


@app.command()
def version() -> None:
    typer.echo("unigrade 0.1.0")
