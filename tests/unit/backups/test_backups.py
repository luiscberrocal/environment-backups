from pathlib import Path

from environment_backups.backups.backups import list_all_projects, get_projects_envs, zip_folder_with_pwd


def test_list_all_projects_with_existing_folders(mocker):
    # Mock os.scandir to return a list of mock directories
    mocker.patch('os.scandir', return_value=[mocker.Mock(is_dir=lambda: True, path='dir1'),
                                             mocker.Mock(is_dir=lambda: True, path='dir2')])
    assert list_all_projects(Path('/some/path')) == ['dir1', 'dir2']


def test_list_all_projects_with_no_folders(mocker):
    # Mock os.scandir to return an empty list
    mocker.patch('os.scandir', return_value=[])
    assert list_all_projects(Path('/some/empty/path')) == []


def test_get_projects_envs_with_valid_data(mocker):
    # Mock list_all_projects to return specific folders
    mocker.patch('environment_backups.backups.backups.list_all_projects', return_value=['project1', 'project2'])
    # Mock Path.exists to return True
    mocker.patch('pathlib.Path.exists', return_value=True)
    expected_result = {
        'project1': {'envs': Path('project1/env_folder')},
        'project2': {'envs': Path('project2/env_folder')}
    }
    assert get_projects_envs(Path('/projects'), ['env_folder']) == expected_result


def test_get_projects_envs_with_no_projects(mocker):
    mocker.patch('environment_backups.backups.backups.list_all_projects', return_value=[])
    assert get_projects_envs(Path('/projects'), ['env_folder']) == {}


def test_zip_folder_with_pwd_without_password(mocker, tmp_path):
    # Set up a temporary directory and files for zipping
    folder_to_zip = tmp_path / "test_folder"
    folder_to_zip.mkdir()
    (folder_to_zip / "test_file.txt").write_text("test content")

    zip_file = tmp_path / "test.zip"

    # Call the function
    zip_folder_with_pwd(zip_file, folder_to_zip)

    # Check if the zip file was created
    assert zip_file.exists()


def test_zip_folder_with_pwd_with_password(mocker, tmp_path):
    # Similar setup as above, but pass a password to the function
    folder_to_zip = tmp_path / "test_folder"
    folder_to_zip.mkdir()
    (folder_to_zip / "test_file.txt").write_text("test content")

    zip_file = tmp_path / "test.zip"

    zip_folder_with_pwd(zip_file, folder_to_zip, password="secret")

    assert zip_file.exists()


def test_zip_folder_with_empty_directory(mocker, tmp_path):
    # Test with an empty directory
    folder_to_zip = tmp_path / "empty_folder"
    folder_to_zip.mkdir()

    zip_file = tmp_path / "empty.zip"

    zip_folder_with_pwd(zip_file, folder_to_zip)

    assert zip_file.exists()
