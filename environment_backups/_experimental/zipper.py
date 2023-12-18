import asyncio
import os
import zipfile
from pathlib import Path


async def async_zip_folder(source_folder: Path, zip_file: Path):
    """
    Asynchronously compresses the contents of a folder into a zip file.

    :param source_folder: Path to the source folder to be zipped.
    :param zip_file: Path to the output zip file.
    """
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, sync_zip_folder, source_folder, zip_file)


def sync_zip_folder(source_folder: Path, zip_file: Path):
    """
    Synchronously compresses the contents of a folder into a zip file.

    :param source_folder: Path to the source folder to be zipped.
    :param zip_file: Path to the output zip file.
    """
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                file_path = Path(root) / file
                zipf.write(file_path, file_path.relative_to(source_folder))


# Example usage
async def main():
    my_downloads = Path.home() / 'Downloads'
    zz_file = Path.home() / 'Documents' / '__zipping_test' / 'tmep.zip'
    await async_zip_folder(my_downloads, zz_file)

if __name__ == '__main__':
    asyncio.run(main())
