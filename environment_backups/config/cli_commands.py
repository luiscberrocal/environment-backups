import sys
from typing import Any, Dict

import click
from rich.pretty import pprint

from environment_backups import CONFIGURATION_MANAGER
from environment_backups.constants import DEFAULT_DATE_FORMAT, DEFAULT_ENV_FOLDER


@click.group()
def config():
    """Configuration entrypoint."""


@click.command()
def init():
    if CONFIGURATION_MANAGER.get_current():
        click.secho(f'Configuration already exists.')
        sys.exit(100)

    configuration_dict = {"application": {}, "configurations": []}

    prompt = 'Date format for backup folder prefix'
    configuration_dict['application']['date_format'] = click.prompt(prompt,
                                                                    default=DEFAULT_DATE_FORMAT)

    prompt = 'Environment folder pattern name to parse. If several separate by a comma'
    env_folders = click.prompt(prompt, default=DEFAULT_ENV_FOLDER)
    configuration_dict['application']['environment folder pattern'] = [x.strip() for x in env_folders.split(',')]

    prompt = 'Default password for zip files'
    configuration_dict['application']['password'] = click.prompt(prompt, default="")
    keep_adding_configs = True
    while keep_adding_configs:
        c = prompt_for_configuration()
        configuration_dict['configurations'].append(c)
        keep_adding_configs = click.confirm('Do you want to add another configuration?')

    pprint(configuration_dict)


config.add_command(init)


def prompt_for_configuration() -> Dict[str, Any]:
    config_dict = {}

    prompt = 'Name of the configuration. Must be unique'
    config_dict['name'] = click.prompt(prompt)

    # TODO Allow using ~/PycharmProjects for example
    prompt = 'Project folder'
    config_dict['project_folder'] = click.prompt(prompt, type=click.Path(exists=True))

    prompt = 'Backup folder'
    config_dict['backup_folder'] = click.prompt(prompt, type=click.Path(exists=False))

    prompt = 'Computer name'
    config_dict['computer_name'] = click.prompt(prompt)

    prompt = 'Google drive support?'
    google_drive_support = click.confirm(prompt)
    if google_drive_support:
        prompt = 'Google drive folder id'
        config_dict['google_drive_folder_id'] = click.prompt(prompt)
        prompt = 'Google authentication file'
        config_dict['google_authentication_file'] = click.prompt(prompt, type=click.Path(exists=False))

    return config_dict
