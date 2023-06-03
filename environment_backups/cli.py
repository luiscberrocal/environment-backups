"""Console script for environment_backups."""
import argparse

import click


@click.command()
def main():
    """Main entrypoint."""
    click.echo("environment-backups")
    click.echo("=" * len("environment-backups"))
    click.echo("CLI Application to backup environment variables.")


def main_arg_parser(parsed_args):
    print(type(parsed_args))
    print(parsed_args)


if __name__ == "__main__":
    """
    backup-environments -f /project/folders -t /target_folder/ -e .envs -e .env
    """
    parser = argparse.ArgumentParser(description="Environment backups")
    parser.add_argument(
        "-e", "--environment-folder",
        type=str,
        nargs="+",
        help="Name of the environment folder to backup"
    )

    parser.add_argument(
        "-f", "--folder",
        type=str,
        help="Folder where the projects are found."
    )
    parser.add_argument(
        "-t", "--target-folder",
        type=str,
        help="Folder to save the zipped files"
    )
    parsed_args = parser.parse_args()
    # main()  # pragma: no cover
    main_arg_parser(parsed_args)
