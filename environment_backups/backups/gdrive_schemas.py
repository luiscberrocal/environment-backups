from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field, HttpUrl


class Installed(BaseModel):
    client_id: str
    project_id: str
    auth_uri: HttpUrl = Field(default="https://accounts.google.com/o/oauth2/auth")
    token_uri: HttpUrl = Field(default="https://oauth2.googleapis.com/token")
    auth_provider_x509_cert_url: HttpUrl = Field(default="https://www.googleapis.com/oauth2/v1/certs")
    client_secret: str
    redirect_uris: List[str] = Field(default=['http://localhost'])


class GoogleConfiguration(BaseModel):
    installed: Installed
