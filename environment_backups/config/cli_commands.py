import sys

import click

from environment_backups import CONFIGURATION_MANAGER


@click.group()
def config():
    """Configuration entrypoint."""


@click.command()
def init():

    if CONFIGURATION_MANAGER.get_current():
        click.secho(f'Configuration already exists.')
        sys.exit(100)



config.add_command(init)
