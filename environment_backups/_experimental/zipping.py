import asyncio
import os
import time
from pathlib import Path

from pyzipper import WZ_AES, AESZipFile, ZIP_DEFLATED

from environment_backups.compression import zip_folder_with_pwd
from environment_backups.exceptions import EnvironmentBackupsError


async def zip_folder_with_pwd_async3(zip_file: Path, folder_to_zip: Path, password: str = None):
    """
    Compresses a folder and creates a zip file with optional password protection.
    @param zip_file: Zip file path
    @param folder_to_zip: Folder to zip
    @param password: Password for the  zip file
    """
    if not folder_to_zip.exists():
        message = f'The target folder to put the zip file {folder_to_zip}does not exist.'
        raise EnvironmentBackupsError(message)

    def zipdir(path: Path, ziph):
        """
        Recursively adds files and directories to a zip file.
        """
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    ziph.write(file_path, os.path.relpath(file_path, path.parent))
        except ValueError as e:
            error_message = f'Error zipping {path}. Error: {e}'
            raise EnvironmentBackupsError(error_message)

    encryption = WZ_AES if password else None

    with AESZipFile(zip_file, 'w', compression=ZIP_DEFLATED, encryption=encryption,
                    strict_timestamps=False) as zf:
        if password:
            pwd = password.encode('utf-8')
            zf.setpassword(pwd)
        zipdir(folder_to_zip, zf)


def tmp_main(fld: Path, backup_folder: Path):
    from environment_backups.backups.backups import list_all_projects
    start = time.time()
    projects = list_all_projects(fld)

    for project in projects:
        zip_file = backup_folder / f'{project}.zip'
        folder_to_zip = fld / f'{project}'
        print(f'Zipping {folder_to_zip} to {zip_file}')
        zip_folder_with_pwd(zip_file=zip_file, folder_to_zip=folder_to_zip)

    elapsed = time.time() - start
    print(f"Folders {len(projects)} elapsed: {elapsed:.2f} seconds")


async def tmp_main_async(fld: Path, backup_folder: Path):
    from environment_backups.backups.backups import list_all_projects
    start = time.time()
    projects = list_all_projects(fld)

    task_list = []
    for project in projects:
        zip_file = backup_folder / f'{project}.zip'
        folder_to_zip = fld / f'{project}'
        print(f'Zipping {folder_to_zip} to {zip_file}')
        task_list.append(zip_folder_with_pwd_async(zip_file=zip_file, folder_to_zip=folder_to_zip))

    result = await asyncio.gather(*task_list)
    print(result)

    elapsed = time.time() - start
    print(f"Folders {len(projects)} elapsed: {elapsed:.2f} seconds")
import asyncio
import os
from pathlib import Path
from pyzipper import WZ_AES, AESZipFile, ZIP_DEFLATED
from environment_backups.exceptions import EnvironmentBackupsError

async def zip_folder_with_pwd_async(zip_file: Path, folder_to_zip: Path, password: str = None):
    """
    Compresses a folder and creates a zip file with optional password protection.
    @param zip_file: Zip file path
    @param folder_to_zip: Folder to zip
    @param password: Password for the zip file
    """
    if not folder_to_zip.exists():
        message = f'The target folder to put the zip file {folder_to_zip} does not exist.'
        raise EnvironmentBackupsError(message)

    def zipdir(path: Path, ziph):
        """
        Recursively adds files and directories to a zip file.
        """
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    ziph.write(file_path, os.path.relpath(file_path, path.parent))
        except ValueError as e:
            error_message = f'Error zipping {path}. Error: {e}'
            raise EnvironmentBackupsError(error_message)

    encryption = WZ_AES if password else None

    # Run the zipping process in an executor
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(
        None,  # Default executor (ThreadPoolExecutor)
        zip_folder,  # Method to execute
        zip_file, folder_to_zip, password, zipdir, encryption
    )

def zip_folder(zip_file, folder_to_zip, password, zipdir, encryption):
    with AESZipFile(zip_file, 'w', compression=ZIP_DEFLATED, encryption=encryption,
                    strict_timestamps=False) as zf:
        if password:
            pwd = password.encode('utf-8')
            zf.setpassword(pwd)
        zipdir(folder_to_zip, zf)


do_sync = False
do_async = True
if __name__ == '__main__':
    my_downloads = Path.home() / 'Downloads'
    my_documents = Path.home() / 'Documents' / '__zipping_test'
    my_documents.mkdir(exist_ok=True)
    if do_sync:
        tmp_main(my_downloads, my_documents)

    if do_async:
        asyncio.run(tmp_main_async(my_downloads, my_documents))
