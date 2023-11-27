from pathlib import Path

from tests.tools import create_projects_folder


def test_create_projects_folder():
    # FIXME User temp_folder
    root_folder = Path(__file__).parent.parent.parent / 'output'
    assert root_folder.exists()
    projects_list = ['project1', 'project2']
    create_projects_folder(root_folder=root_folder, projects_folders=projects_list)

    projects_folder = root_folder / 'MyProjectsForTests'
    assert projects_folder.exists()
    for project in projects_list:
        assert (projects_folder / project).exists()
        # TODO check file
