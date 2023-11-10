"""Console script for environment_backups."""
import sys
from platform import python_version
from typing import List

import click
from rich.panel import Panel

from environment_backups import CONFIGURATION_MANAGER, CONSOLE
from environment_backups import __version__ as current_version
from environment_backups.backups.cli_commands import backup


@click.group()
def main():
    """Main entrypoint."""
    click.echo("environment-backups")
    click.echo("=" * len("environment-backups"))
    click.echo("CLI Application to backup environment variables.")


@click.command()
def about():
    app_name = CONFIGURATION_MANAGER.APP_NAME.replace('-', ' ').title()
    content: List[str] = []
    content.append(f'Operating System: {sys.platform}')
    content.append(f'Python : {python_version()}')
    content.append(f'Configuration file: {CONFIGURATION_MANAGER.config_file}')
    panel = Panel('\n'.join(content), title=app_name, subtitle=f"version: {current_version}")
    CONSOLE.print(panel)


if __name__ == "__main__":
    """
    environment-backups -p /project/folders -b /target_folder/
    """
    # main()  # pragma: no cover

main.add_command(backup)
main.add_command(about)

