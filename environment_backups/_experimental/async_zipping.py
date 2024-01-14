import asyncio
import random
import time
from pathlib import Path
from typing import Any, Iterable

from environment_backups.zipper import sync_zip_folder_with_pwd


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
    # zipping_wait = random.random() * 5
    # await asyncio.sleep(zipping_wait)
    start = time.perf_counter()
    # zipped_file = folder / f'{folder.stem}.zip'
    z_file = sync_zip_folder_with_pwd(folder=folder, zip_file=zip_file)
    # print(f'Zipped {zipped_file} took {zipping_wait} seconds')
    elapsd = time.perf_counter() - start
    # print(f'Zipped {zipped_file} took {zipping_wait} seconds')
    print(f'Zipped {zip_file} took {elapsd} seconds')
    # Uploading
    emulate_upload = False
    if emulate_upload:
        print(f'Uploading {zip_file}')
        upload_wait = elapsed * 3  # random.random() * 5
        await asyncio.sleep(upload_wait)
        print(f'Uploaded {zip_file} took {upload_wait} seconds')
    return zip_file


async def do_backups(files: Iterable[Path], folder: Path) -> Any:
    task_list = []
    for file in files:
        task_list.append(async_zipping(file, folder))
    results = await asyncio.gather(*task_list)
    return results


async def zip_multiple_folders(folders: Iterable[Path], backup_folder: Path) -> Any:
    task_list = []
    for f in folders:
        zip_file = backup_folder / f'{f.stem}.zip'
        task_list.append(async_zipping_folder(folder=f, zip_file=zip_file))
    results = await asyncio.gather(*task_list)
    return results


if __name__ == '__main__':
    """For ziping it is better to use sync."""
    start_time = time.time()
    data_path = Path().home() / 'Downloads'
    source_folders = [f for f in data_path.iterdir() if f.is_dir()]
    zip_results = asyncio.run(zip_multiple_folders(folders=source_folders, backup_folder=data_path))
    elapsed = time.time() - start_time
    print(f'Zipping took {elapsed} seconds')
    print(zip_results)
    # Cleanup
    for zip_result in zip_results:
        zip_result.unlink()
    # Doing operation synchronously
    start_time = time.time()
    sync_results = []
    for folder in source_folders:
        z = data_path / f'{folder.name}.zip'
        zip_result = sync_zip_folder_with_pwd(folder=folder, zip_file=z)
        zip_results.append(zip_result)
    elapsed_sync = time.time() - start_time
    print(f'Zipping took {elapsed_sync} seconds')


# f = [Path('file1'), Path('file2'), Path('file3'), Path('file4')]
# fldr = Path('folder1')
# t = asyncio.run(do_backups(f, fldr))
