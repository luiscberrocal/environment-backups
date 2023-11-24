#!/usr/bin/env python
"""Tests for `environment_backups` package."""

from click.testing import CliRunner

from environment_backups import cli


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    result_lines = result.output.split('\n')
    expected_lines = [
        "Usage: main [OPTIONS] COMMAND [ARGS]...",
        "",
        "  Main entrypoint.",
        "",
        "Options:",
        "  --help  Show this message and exit.",
        "",
        "Commands:",
        "  about",
        "  backup",
        "  config  Configuration entrypoint.",
        ""
    ]
    assert len(result_lines) == len(expected_lines)
    assert result.exit_code == 0
    for i, line in enumerate(result_lines):
        assert line == expected_lines[i]


def test_help():
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ['--help'])

    assert help_result.exit_code == 0
    output_lines = help_result.output.split('\n')

    # ------------------------------
    var_name = 'output_lines'
    var_value = eval(var_name)
    from pathlib import Path
    import json
    file = Path(__name__) / f'{var_name}.json'
    with open(file, 'w') as f:
        json.dump(var_value, f, indent=4)
    print(f'Saved file')
    # ------------------------------------
