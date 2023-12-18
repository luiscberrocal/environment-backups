import asyncio
import os
import time
from pathlib import Path
from typing import List

import pyzipper


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


async def zip_folders_with_pwd(source_folder: Path, backup_folder: Path, password: str = None) -> List[Path]:
    zipped_files = []
    for item in source_folder.iterdir():
        if item.is_dir():
            zip_file_path = backup_folder / f"{item.name}.zip"
            print(f'Zipping {item.name} to {zip_file_path}')
            await zip_folder_with_pwd_async(item, zip_file_path, password)
            zipped_files.append(zip_file_path)
    return zipped_files


# Example usage
async def main():
    source = Path.home() / 'Downloads'
    backup = Path.home() / 'Documents' / '__zipping_test'

    zipped_files = await zip_folders_with_pwd(source, backup, None)
    print("Zipped files:", zipped_files)


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    print(f'Elapsed: {(time.time() - start):.2f} seconds.')
