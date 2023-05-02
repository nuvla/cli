"""
Auxiliary module to build the CLI commands
"""

import typer

from nuvla_cli.entity_action_cmd import edge, fleet, user


def build_entity_action(app_cli: typer.Typer) -> None:
    """
    Build the entity-action command around cli_app parameter
    :param app_cli: Main CLI app to build the commands upon
    :return: None
    """
    app_cli.add_typer(edge.app, name='edge', help='Edge management commands')
    app_cli.add_typer(fleet.app, name='fleet', help='Fleet management commands')
    app_cli.add_typer(user.app, name='user', help='User management commands')
    app_cli.registered_commands += user.app.registered_commands
