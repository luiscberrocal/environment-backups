"""Console script for environment_backups."""

import click


@click.command()
def main():
    """Main entrypoint."""
    click.echo("environment-backups")
    click.echo("=" * len("environment-backups"))
    click.echo("CLI Application to backup environment variables.")


if __name__ == "__main__":
    """
    environment-backups -f /project/folders -t /target_folder/ -e .envs -e .env
    """
    # main()  # pragma: no cover
