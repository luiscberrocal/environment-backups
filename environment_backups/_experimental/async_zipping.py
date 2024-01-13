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


async def do_backups(files: Iterable[Path], folder: Path) -> Any:
    task_list = []
    for file in files:
        task_list.append(async_zipping(file, folder))
    results = await asyncio.gather(*task_list)
    return results


if __name__ == '__main__':
    f = [Path('file1'), Path('file2'), Path('file3'), Path('file4')]
    fldr = Path('folder1')
    t = asyncio.run(do_backups(f, fldr))
