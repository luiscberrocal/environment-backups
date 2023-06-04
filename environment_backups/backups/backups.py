import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Tuple

from pyzipper import AESZipFile, ZIP_DEFLATED, WZ_AES


def list_all_projects(project_folder: Path) -> List[str]:
    folders = [x.path for x in os.scandir(project_folder) if x.is_dir()]
    return folders


def get_projects_envs(project_folder: Path, environment_folders: List[str]) -> Dict[str, Any]:
    folders = list_all_projects(project_folder)
    folder_dict = dict()
    for folder in folders:
        path = Path(folder)
        for environment_folder in environment_folders:
            envs = path / environment_folder
            if envs.exists():
                folder_dict[path.name] = {'envs': envs}
    return folder_dict


def zip_folder_with_pwd(zip_file: Path, folder_to_zip: Path, password: str = None):
    """
    Compresses a folder and creates a zip file with optional password protection.
    @param zip_file:
    @param folder_to_zip:
    @param password:

    """

    def zipdir(path: Path, ziph):
        """
        Recursively adds files and directories to a zip file.
        """

        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                ziph.write(file_path, os.path.relpath(file_path, path.parent))

    encryption = WZ_AES if password else None

    with AESZipFile(zip_file, 'w', compression=ZIP_DEFLATED, encryption=encryption) as zf:
        if password:
            pwd = password.encode('utf-8')
            zf.setpassword(pwd)
        zipdir(folder_to_zip, zf)


def backup_envs(project_folder: Path, backup_folder: Path,
                environment_folders: List[str], password: str = None,
                date_format='%Y%m%d_%H', ) -> Tuple[List[Path], Path]:
    project_envs_dict = get_projects_envs(project_folder, environment_folders)
    timestamp = datetime.now().strftime(date_format)
    b_folder = backup_folder / timestamp
    b_folder.mkdir(exist_ok=True)
    zip_list = []
    for project, v in project_envs_dict.items():
        zip_file = b_folder / f'{project}.zip'
        zip_folder_with_pwd(zip_file, v['envs'], password=password)
        zip_list.append(zip_file)
    return zip_list, b_folder
