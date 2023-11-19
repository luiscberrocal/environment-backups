"""Top-level package for Environment backups."""

__author__ = """Luis C. Berrocal"""
__email__ = 'luis.berrocal.1942@gmail.com'
__version__ = '0.4.1'

from rich.console import Console
from environment_backups.config.configuration import ConfigurationManager

CONFIGURATION_MANAGER = ConfigurationManager()

CONSOLE = Console()
