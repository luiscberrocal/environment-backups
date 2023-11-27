from pathlib import Path
from typing import List


def create_projects_folder(*, root_folder: Path,
                           projects_folder_name: str = 'MyProjectsForTests',
                           projects_folders: List[str] = None,
                           env_folders: List[str]= ['.envs']):
    if projects_folders is None:
        projects_folders = ['project1']
    projects_folder = root_folder / projects_folder_name
    projects_folder.mkdir()

    for folder_name in projects_folders:
        project_folder = projects_folder / folder_name
        project_folder.mkdir()
        for env_name in env_folders:
            env_folder = project_folder / env_name
            env_folder.mkdir()
            config_file = env_folder / 'dummy.txt'
            config_file.touch()
