import asyncio
import random
from pathlib import Path
from typing import Iterable, Any


async def async_zipping(file: Path, folder: Path) -> Path:
    print(f"Zipping {file}")
    zipping_wait = random.random() * 5
    await asyncio.sleep(zipping_wait)
    zipped_file = folder / f'{file.stem}.zip'
    print(f'Zipped {zipped_file} took {zipping_wait} seconds')
    print(f'Uploading {zipped_file}')
    upload_wait = random.random() * 5
    await asyncio.sleep(upload_wait)
    print(f'Uploaded {zipped_file} took {upload_wait} seconds')
    return zipped_file


async def async_zipping_folder(folder: Path, zip_file: Path) -> Path:
    print(f"Zipping {folder}")
    zipping_wait = random.random() * 5
    await asyncio.sleep(zipping_wait)
    zipped_file = folder / f'{folder.stem}.zip'
    print(f'Zipped {zipped_file} took {zipping_wait} seconds')
    # Uploading
    print(f'Uploading {zipped_file}')
    upload_wait = random.random() * 5
    await asyncio.sleep(upload_wait)
    print(f'Uploaded {zipped_file} took {upload_wait} seconds')
    return zipped_file


async def do_backups(files: Iterable[Path], folder: Path) -> Any:
    task_list = []
    for file in files:
        task_list.append(async_zipping(file, folder))
    results = await asyncio.gather(*task_list)
    return results


async def zip_multiple_folders(folders: Iterable[Path], folder: Path) -> Any:
    task_list = []
    for f in folders:
        zip_file = folder / f'{f.stem}.zip'
        task_list.append(async_zipping_folder(folder=f, zip_file=zip_file))
    results = await asyncio.gather(*task_list)
    return results


if __name__ == '__main__':
    data_path = Path().home() / 'Downloads'
    source_folders = [f for f in data_path.iterdir() if f.is_dir()]
    zip_results = asyncio.run(zip_multiple_folders(folders=source_folders, folder=data_path))
    print(zip_results)
# f = [Path('file1'), Path('file2'), Path('file3'), Path('file4')]
# fldr = Path('folder1')
# t = asyncio.run(do_backups(f, fldr))
