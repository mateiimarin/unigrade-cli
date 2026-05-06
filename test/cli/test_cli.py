"""Test the unigrade CLI."""

from typer.testing import CliRunner

from unigrade.cli import app

runner = CliRunner()


def test_version_command_shows_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "unigrade 0.1.0" in result.output
