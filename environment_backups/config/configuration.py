import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List

import toml

from .utils import backup_file
from .. import exceptions


class ConfigurationManager:
    DEFAULT_CONFIG_FOLDER_NAME = '.environment_backups'
    DEFAULT_CONFIG_FILENAME = 'configuration.toml'
    APP_NAME = DEFAULT_CONFIG_FOLDER_NAME[1:].replace('_', '-')

    def __init__(self, config_folder: Optional[Path] = None,
                 config_filename: Optional[str] = None):
        if config_folder is None:
            self.config_folder = Path().home() / self.DEFAULT_CONFIG_FOLDER_NAME
        else:
            self.config_folder = config_folder
        if config_filename is None:
            self.config_file = self.config_folder / self.DEFAULT_CONFIG_FILENAME
        else:
            self.config_file = self.config_folder / config_filename

        self.config_backup_folder = self.config_folder / 'backups'
        self.logs_folder = self.config_folder / 'logs'

        self.app_folder = Path().home() / 'Documents' / self.APP_NAME
        self.username = os.getlogin()
        self.prep_config()

    def get_sample_config(self) -> Dict[str, Any]:
        data = {
            'application': {
                'folder': {
                    'folder': str(self.app_folder),
                    'prompt': 'Application folder'
                },
                'output_folder': {
                    'folder': str(self.app_folder / 'output'),
                    'prompt': 'Input folder'
                },
                'processed_folder': {
                    'folder': str(self.app_folder / 'processed'),
                    'prompt': 'Processed folder'
                },
                'input_folder': {
                    'folder': str(self.app_folder / 'input'),
                    'prompt': 'Input folder'
                },
                'timestamp_format': '%Y%m%d_%H%M%S'
            },
            'database': {
                'db_file': {
                    'filename': str(self.config_folder / 'invoicing_db.json'),
                    'prompt': 'JSON database file'
                }
            },
            'logs': {
                'folder': str(self.logs_folder),
                'filename': f'{self.APP_NAME}.log',
                'backup_count': 3
            },
            'google': {
                'secrets_file': {
                    'filename': str(self.config_folder / 'client_secrets.json'),
                    'prompt': 'Client secrets file'
                },
                'scanned_folder': {
                    "id": "",
                    "name": "EMR Facturas Scanned",
                    'prompt': 'Google drive scanned folder name'
                }
            },
        }
        return data

    def prep_config(self):
        self.config_folder.mkdir(exist_ok=True)
        self.config_backup_folder.mkdir(exist_ok=True)
        self.logs_folder.mkdir(exist_ok=True)
        if not self.config_file.exists():
            tmp_config = self.get_sample_config()
            self.write_configuration(tmp_config)

    def write_configuration(self, config_data: Dict[str, Any], overwrite: bool = False, ) -> None:
        if self.config_file.exists() and not overwrite:
            raise Exception('Cannot overwrite config file.')
        with open(self.config_file, 'w') as f:
            toml.dump(config_data, f)

    def get_configuration(self) -> Dict[str, Any]:
        if not self.config_folder.exists():
            error_message = 'No configuration file found. Run  config.'
            raise exceptions.ConfigurationError(error_message)

        with open(self.config_file, 'r') as f:
            configuration = toml.load(f)
        return configuration

    def export_to_json(self, export_file: Path) -> None:
        config = self.get_configuration()
        with open(export_file, 'w') as f:
            json.dump(config, f)

    def backup(self) -> Path:
        backup_filename = backup_file(self.config_file, self.config_backup_folder)
        return backup_filename

    def delete(self) -> Path:
        backup_filename: Path = self.backup()
        self.config_file.unlink(missing_ok=True)
        return backup_filename

    def get_configuration_folders(self) -> Dict[str, Path]:
        config = self.get_configuration()
        folders = dict()
        for key, folder_option in config['application'].items():
            if not isinstance(folder_option, dict):
                continue
            if folder_option.get('folder') is None:
                continue
            folders[key] = Path(folder_option['folder'])
        return folders

    @classmethod
    def get_current(cls):
        config = cls()
        return config.get_configuration()
