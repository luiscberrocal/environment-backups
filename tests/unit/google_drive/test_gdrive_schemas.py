from pydantic import BaseModel

from environment_backups.google_drive.gdrive_schemas import GoogleCredentialsToken


class DummyObject(BaseModel):
    name: str
    age: int


class TestGoogleCredentialsToken:

    def test_save(self, tmp_path):
        dummy = DummyObject(name='My name', age=4)
        dummy_file = tmp_path / 'cred.token'
        gdrive_credential_token = GoogleCredentialsToken(token_file=dummy_file)
        assert not dummy_file.exists()
        gdrive_credential_token.save(dummy)
        assert dummy_file.exists()
