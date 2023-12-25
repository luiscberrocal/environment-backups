import asyncio
import os
import shutil
from pathlib import Path
from typing import List

import pyzipper

from environment_backups.backups.backups import list_all_projects
from environment_backups.compression import zip_folder_with_pwd


async def zip_folder_with_pwd_async(folder: Path, zip_file: Path, password: str = None):
    """
    Asynchronously compresses a single folder into a zip file with optional password protection.
    """
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(
        None,
        sync_zip_folder_with_pwd,
        folder,
        zip_file,
        password
    )


def sync_zip_folder_with_pwd(folder: Path, zip_file: Path, password: str = None):
    """
    Synchronously compresses a single folder into a zip file with optional password protection.
    """
    with pyzipper.AESZipFile(zip_file, 'w', compression=pyzipper.ZIP_DEFLATED, strict_timestamps=False) as zipf:
        if password:
            zipf.setpassword(password.encode('utf-8'))
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = Path(root) / file
                zipf.write(file_path, file_path.relative_to(folder.parent))


async def zip_folders_with_pwd_async(source_folder: Path, backup_folder: Path, password: str = None) -> List[Path]:
    zipping_tasks = []
    zipped_files = []

    for item in source_folder.iterdir():
        if item.is_dir():
            zip_file_path = backup_folder / f"{item.name}.zip"
            print(f'Zipping {item.name} to {zip_file_path}')
            zipping_tasks.append(zip_folder_with_pwd_async(item, zip_file_path, password))
            zipped_files.append(zip_file_path)

    await asyncio.gather(*zipping_tasks)
    return zipped_files


def main_sync(source: Path, backup: Path, password: str):
    # source = Path.home() / 'Downloads'
    # backup = Path.home() / 'Documents' / '__zipping_test'
    # if backup.exists():
    #     shutil.rmtree(backup)
    #     backup.mkdir()
    start = time.time()
    projects = list_all_projects(source)

    for project in projects:
        zip_file = backup / f'{project}.zip'
        folder_to_zip = source / f'{project}'
        print(f'Zipping {folder_to_zip} to {zip_file}')
        zip_folder_with_pwd(zip_file=zip_file, folder_to_zip=folder_to_zip)

    elapsed = time.time() - start
    print(f"Folders {len(projects)} elapsed: {elapsed:.2f} seconds")


# Example usage
async def main(source: Path, backup: Path, password: str):
    # source = Path.home() / 'Downloads'
    # backup = Path.home() / 'Documents' / '__zipping_test'
    # if backup.exists():
    #     shutil.rmtree(backup)
    #     backup.mkdir()

    zipped_files = await zip_folders_with_pwd_async(source, backup, password)
    print("Zipped files:", zipped_files)


if __name__ == '__main__':
    import time
    source_folder = Path.home() / 'PycharmProjects'
    backup_folder = Path.home() / 'Documents' / '__zipping_test'

    if backup_folder.exists():
        shutil.rmtree(backup_folder)
        backup_folder.mkdir()

    start = time.time()
    asyncio.run(main())
    print(f'Async time elapsed: {(time.time() - start):.2f} seconds.')

    main_sync()
