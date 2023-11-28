import shutil
from pathlib import Path
from typing import List, Tuple


def create_projects_folder_for_tests(*, root_folder: Path,
                                     projects_folder_name: str = 'MyProjectsForTests',
                                     projects_folders: List[str] = None,
                                     env_folders: List[str] = None,
                                     env_file_count: int = 1) -> Tuple[Path, List[Path]]:
    if projects_folders is None:
        projects_folders = ['project1']
    if env_folders is None:
        env_folders = ['.envs']

    projects_folder = root_folder / projects_folder_name
    projects_folder.mkdir()
    environment_files = []
    for folder_name in projects_folders:
        project_folder = projects_folder / folder_name
        project_folder.mkdir()
        for env_name in env_folders:
            env_folder = project_folder / env_name
            env_folder.mkdir()
            for i in range(env_file_count):
                config_file = env_folder / f'dummy{i}.txt'
                config_file.touch()
                environment_files.append(config_file)
    return projects_folder, environment_files

    # shutil.rmtree(project_folder)
