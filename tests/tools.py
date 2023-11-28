from pathlib import Path
from typing import List, Tuple

from environment_backups.config.schemas import Application, Configuration, ApplicationConfiguration


def create_projects_folder_for_tests(*, root_folder: Path,
                                     projects_folder_name: str = 'MyProjectsForTests',
                                     projects_folders: List[str] = None,
                                     env_folders: List[str] = None,
                                     env_file_count: int = 1) -> Tuple[Path, List[Path]]:
    """
      Creates a nested directory structure for testing, including project and environment folders.

      @param root_folder: The root directory where the projects folder will be created.
      @type root_folder: Path

      @param projects_folder_name: Name of the main projects folder. Defaults to 'MyProjectsForTests'.
      @type projects_folder_name: str, optional

      @param projects_folders: Names of individual project folders. Defaults to ['project1'] if not provided.
      @type projects_folders: List[str], optional

      @param env_folders: Names of environment folders within each project folder. Defaults to ['.envs'] if not provided.
      @type env_folders: List[str], optional

      @param env_file_count: Number of dummy config files in each environment folder. Defaults to 1 if not provided.
      @type env_file_count: int, optional

      @return: A tuple containing the path to the main projects folder and a list of paths to the created dummy
       configuration files.
      @rtype: Tuple[Path, List[Path]]

      The function creates a structure as follows:
      root_folder/
          projects_folder_name/
              project1/
                  .envs/
                      dummy0.txt
                      ...
              project2/
                  .envs/
                      dummy0.txt
                      ...
              ...
      """

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


def build_valid_configuration_for_tests(*, projects_folder: Path, backup_folder: Path = None,
                                        google_support: bool = True) -> ApplicationConfiguration:
    if backup_folder is None:
        backup_folder = projects_folder / 'environment_backups'

    app = Application()
    config_name = 'test_config'

    cfg = Configuration(name=config_name,
                        projects_folder=projects_folder,
                        backup_folder=backup_folder,
                        computer_name='deep-space9')
    if google_support:
        cfg.google_drive_folder_id = 'ddg'
        cfg.google_authentication_file = projects_folder / 'dummy_google.json'

    application_configuration = ApplicationConfiguration(application=app, configuration=[cfg])

    return application_configuration
