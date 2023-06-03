"""Console script for environment_backups."""
import argparse
from pathlib import Path

import click

from environment_backups._legacy.pretty_print import print_success
from environment_backups.backups.backups import backup_envs


@click.command()
def main():
    """Main entrypoint."""
    click.echo("environment-backups")
    click.echo("=" * len("environment-backups"))
    click.echo("CLI Application to backup environment variables.")


def main_arg_parser():
    parser = argparse.ArgumentParser(description="Environment backups")
    parser.add_argument(
        "-e", "--environment-folder",
        type=str,
        nargs="+",
        help="Name of the environment folder to backup",
        default=['.envs']
    )

    parser.add_argument(
        "-f", "--folder",
        type=Path,
        help="Folder where the projects are found.",
        required=True
    )
    parser.add_argument(
        "-t", "--target-folder",
        type=Path,
        help="Folder to save the zipped files",
        required=True
    )
    parsed_args = parser.parse_args()
    # print(parsed_args)

    zip_files, ts_backup_folder = backup_envs(project_folder=parsed_args.folder,
                                              backup_folder=parsed_args.target_folder,
                                              environment_folders=parsed_args.environment_folder)
    for i, zf in enumerate(zip_files, 1):
        print_success(f'{i} {zf.name}')
    print_success(f'Wrote {len(zip_files)} zip files')
    print_success(f'Output folder: {ts_backup_folder}')

if __name__ == "__main__":
    """
    environment-backups -f /project/folders -t /target_folder/ -e .envs -e .env
    """
    # main()  # pragma: no cover
