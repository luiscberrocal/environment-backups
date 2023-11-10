import shutil
from pathlib import Path

import pytest


@pytest.fixture(scope='session')
def output_folder() -> Path:
    folder = Path(__file__).parent.parent / 'output'
    return folder


@pytest.fixture(scope='session')
def tmp_config_folder(output_folder) -> Path:
    c_folder = output_folder / 'tmp_config_folder'
    c_folder.mkdir()
    yield c_folder
    shutil.rmtree(c_folder)


@pytest.fixture(scope='session')
def fixtures_folder() -> Path:
    folder = Path(__file__).parent / 'fixtures'
    return folder
