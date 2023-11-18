from click.testing import CliRunner

import environment_backups

from environment_backups.config.cli_commands import config

def test_init_existing_values(mocker):
    mocker.patch('environment_backups.config.cli_commands.CONFIGURATION_MANAGER.get_current',
                 return_value={'hello': 'world'})
    runner = CliRunner()
    result = runner.invoke(environment_backups.config.cli_commands.config, ['init'])
    output_lines = result.output.split('\n')

    assert len(output_lines) == 1
    assert output_lines[0] == 'Configuration already exists.'
    assert result.exit_code == 100


def test_init_command(mock_config_manager):
    runner = CliRunner()
    mock_inputs = '\n'.join(['%Y-%m-%d', 'env_folder', 'password', 'No', 'Yes'])
    result = runner.invoke(config, ['init'], input=mock_inputs)

    assert result.exit_code == 0
    assert 'Init configuration file' in result.output
    # Assert if the mock CONFIGURATION_MANAGER was used correctly
    mock_config_manager.set_configuration.assert_called_once()
    if "Yes" in mock_inputs.split('\n'):
        mock_config_manager.save.assert_called_once()