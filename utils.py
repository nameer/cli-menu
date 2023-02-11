from typing import Any


def success(message: str) -> str:
    return f"[green]{message}[/green]"


def warning(message: str) -> str:
    return f"[yellow]{message}[/yellow]"


def error(message: str) -> str:
    return f"[red]{message}[/red]"


def bad_input(value: Any) -> str:
    return f"[bold]{value}[/bold]"


def stress(value: Any) -> str:
    return f"[italic]{value}[/italic]"
