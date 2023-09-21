from pathlib import Path

import click

from environment_backups.backups.backups import backup_envs
from environment_backups.exceptions import EnvironmentBackupsError


@click.command()
@click.option('projects_folder', '-p', '--projects-folder', type=click.Path(exists=True), required=False)
@click.option('backup_folder', '-b', '--backup-folder', type=click.Path(exists=False), required=False)
def backup(projects_folder: Path, backup_folder: Path):
    if projects_folder is None:
        raise EnvironmentBackupsError('Missing projects folder')
    else:
        projects_folder = Path(projects_folder)
    if backup_folder is None:
        raise EnvironmentBackupsError('Missing backup folder')
    else:
        backup_folder = Path(backup_folder)
    # TODO Add to configuration
    environment_folders = ['.envs']

    zip_list, b_folder = backup_envs(projects_folder=projects_folder, backup_folder=backup_folder,
                                     environment_folders=environment_folders)
    for i, zip_file in enumerate(zip_list, 1):
        click.secho(f'{i}. {zip_file.name}', fg='green')
