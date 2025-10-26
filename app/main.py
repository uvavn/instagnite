import importlib
import pkgutil
import typer

from app.core.registry import get_registry


ignite = typer.Typer()


def load_commands() -> None:
    import app.commands

    for _, module_name, _ in pkgutil.iter_modules(app.commands.__path__):
        importlib.import_module(f"app.commands.{module_name}")


def register_with_typer() -> None:
    group_apps: dict[str, typer.Typer] = {}

    for group, name, func in get_registry():
        if group not in group_apps:
            group_apps[group] = typer.Typer()
            ignite.add_typer(group_apps[group], name=group)
        group_apps[group].command(name)(func)


def main() -> None:
    load_commands()
    register_with_typer()
    ignite()