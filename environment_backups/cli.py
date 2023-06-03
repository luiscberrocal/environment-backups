"""Console script for environment_backups."""
import argparse
from pathlib import Path

import click


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
    print(type(parsed_args))
    print(parsed_args)


if __name__ == "__main__":
    """
    environment-backups -f /project/folders -t /target_folder/ -e .envs -e .env
    """
    # main()  # pragma: no cover
