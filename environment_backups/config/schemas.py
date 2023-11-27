from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel


class Application(BaseModel):
    environment_folder_pattern: List[str]
    date_format: str
    password: str


class Configuration(BaseModel):
    name: str
    project_folder: Path
    backup_folder: Path
    computer_name: str
    google_drive_folder_id: Optional[str]
    google_authentication_file: Optional[Path]


class ApplicationConfiguration(BaseModel):
    application: Application
    configurations: List[Configuration]
