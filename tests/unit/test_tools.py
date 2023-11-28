import shutil
from pathlib import Path

import pytest

from tests.tools import create_projects_folder_for_tests, build_valid_configuration_for_tests


def test_create_projects_folder(tmp_path):
    root_folder = tmp_path # Path(__file__).parent.parent.parent / 'output'
    assert root_folder.exists()
    projects_list = ['project1', 'project2']
    projects_folder, config_files = create_projects_folder_for_tests(root_folder=root_folder,
                                                                     projects_folders=projects_list)

    projects_folder = root_folder / 'MyProjectsForTests'
    assert projects_folder.exists()
    for project in projects_list:
        assert (projects_folder / project).exists()

    for config_file in config_files:
        assert config_file.exists()
    shutil.rmtree(projects_folder)

def test_build_valid_configuration_for_tests():
    config = build_valid_configuration_for_tests()
    pytest.fail('Not implemented')
