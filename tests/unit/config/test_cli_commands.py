from click.testing import CliRunner

import environment_backups
from environment_backups.config.cli_commands import config


def test_init_existing_values(mocker):
    mocker.patch(
        'environment_backups.config.cli_commands.CONFIGURATION_MANAGER.get_current', return_value={'hello': 'world'}
    )
    runner = CliRunner()
    result = runner.invoke(environment_backups.config.cli_commands.config, ['init'])
    output_lines = result.output.split('\n')

    assert len(output_lines) == 1
    assert output_lines[0] == 'Configuration already exists.'
    assert result.exit_code == 100


def test_init_command(mock_config_manager, tmp_path):
    mock_config_manager.get_current.return_value = {}
    runner = CliRunner()
    mock_inputs = '\n'.join(
        ['%Y-%m-%d', '.envs', '', 'my_config_name', str(tmp_path), str(tmp_path), "my_computer_name", 'N', 'N', 'y']
    )
    result = runner.invoke(config, ['init'], input=mock_inputs)

    assert result.exit_code == 0
    assert 'Init configuration file' in result.output
    # Assert if the mock CONFIGURATION_MANAGER was used correctly
    mock_config_manager.set_configuration.assert_called_once()
    if "Yes" in mock_inputs.split('\n'):
        mock_config_manager.save.assert_called_once()


def test_reset_delete(mock_config_manager):
    mock_config_manager.get_current.return_value = {}
    runner = CliRunner()
    mock_inputs = '\n'.join(['Y'])
    result = runner.invoke(config, ['reset'], input=mock_inputs)

    assert result.exit_code == 0
    lines = result.output.split('\n')
    assert len(lines) == 3
    assert 'By resetting the configuration the' in lines[0]
    assert 'Configuration file deleted. A backup was created ' in lines[1]
