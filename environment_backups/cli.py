"""Console script for environment_backups."""

import click

from environment_backups.backups.cli_commands import backup


@click.group()
def main():
    """Main entrypoint."""
    click.echo("environment-backups")
    click.echo("=" * len("environment-backups"))
    click.echo("CLI Application to backup environment variables.")


if __name__ == "__main__":
    """
    environment-backups -p /project/folders -b /target_folder/
    """
    # main()  # pragma: no cover

main.add_command(backup)
