from click.testing import CliRunner

import environment_backups


def test_init_existing_values(mocker):
    mocker.patch('environment_backups.config.cli_commands.CONFIGURATION_MANAGER.get_current',
                 return_value={'hello': 'world'})
    runner = CliRunner()
    result = runner.invoke(environment_backups.config.cli_commands.config, ['init'])
    output_lines = result.output.split('\n')

    assert len(output_lines) == 1
    assert output_lines[0] == 'Configuration already exists.'
    assert result.exit_code == 100



