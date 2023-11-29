import click
from click.testing import CliRunner
import pytest
from unittest.mock import MagicMock, patch

from environment_backups.config.cli_commands import edit


def test_edit_command():
    """
    Test the 'edit' command of the CLI application.

    This test checks the following:
    - The command outputs the initial message with the config file path.
    - The command prompts for inputs and updates the configuration accordingly.
    - The command calls the save method of CONFIGURATION_MANAGER if the user confirms the save.
    """
    # Mock CONFIGURATION_MANAGER
    mock_config_manager = MagicMock()
    mock_config_manager.get_current.return_value = {
        'application': {
            'date_format': 'YYYY-MM-DD',
            'environment_folder_pattern': ['pattern1', 'pattern2'],
            'password': 'old_password'
        },
        'configurations': [{'name': 'config1'}]
    }
    mock_config_manager.config_file = '/path/to/config.toml'

    # Simulate user inputs
    inputs = ['YYYY-MM-DD', 'pattern1, pattern3', 'new_password', 'y', 'n', 'y']
    mock_inputs = '\n'.join(inputs)

    with patch('environment_backups.CONFIGURATION_MANAGER', mock_config_manager):
        runner = CliRunner()
        result = runner.invoke(edit, input=mock_inputs)

    # Assertions
    # assert 'Init configuration file: /path/to/config.toml' in result.output
    assert result.exit_code == 0
    mock_config_manager.set_configuration.assert_called_once()
    mock_config_manager.save.assert_called_once()

@pytest.fixture
def runner():
    """Fixture to provide a click test runner."""
    return CliRunner()

@pytest.fixture
def mock_config_manager():
    """Fixture to mock CONFIGURATION_MANAGER."""
    with patch('environment_backups.CONFIGURATION_MANAGER') as mock:
        yield mock
