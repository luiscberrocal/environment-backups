from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from environment_backups.config.cli_commands import edit
from tests.factories import configuration_factory


def test_edit_command(tmp_path):
    """
    Test the 'edit' command of the CLI application.

    This test checks the following:
    - The command outputs the initial message with the config file path.
    - The command prompts for inputs and updates the configuration accordingly.
    - The command calls the save method of CONFIGURATION_MANAGER if the user confirms the save.
    """
    # Mock CONFIGURATION_MANAGER
    mock_config_manager = MagicMock()
    
    projects_folder = tmp_path / 'MyProjects'
    app_configuration = configuration_factory(projects_folder=projects_folder, google_support=False)
    app_configuration_dict = app_configuration.model_dump(mode='json')
    mock_config_manager.get_current.return_value = app_configuration_dict

    mock_config_manager.config_file = '/path/to/config.toml'

    # Simulate user inputs
    inputs = ['YYYY-MM-DD', 'pattern1, pattern3', 'new_password', 'y', '', '', '', '', 'y']
    mock_inputs = '\n'.join(inputs)

    with patch('environment_backups.config.cli_commands.CONFIGURATION_MANAGER', mock_config_manager):
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
