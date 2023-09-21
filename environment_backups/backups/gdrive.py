import json
import pickle
from pathlib import Path

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from environment_backups.exceptions import UploadError


class GDrive:
    SCOPES = ['https://www.googleapis.com/auth/drive']

    def __init__(self, secrets_file: Path):
        self.secrets_file = secrets_file
        token_file = secrets_file.parent / 'token.pickle'
        creds = self.get_g_drive_credentials(token_file)
        self.service = build('drive', 'v3', credentials=creds)

    def get_g_drive_credentials(self, token_file):
        creds = None
        # The file token.pickle stores the
        # user's access and refresh tokens. It is
        # created automatically when the authorization
        # flow completes for the first time.
        # Check if file token.pickle exists
        if token_file.exists():
            # Read the token from the file and
            # store it in the variable creds
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        # If no valid credentials are available,
        # request the user to log in.
        if not creds or not creds.valid:

            # If token is expired, it will be refreshed,
            # else, we will request a new one.
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(str(self.secrets_file), self.SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the access token in token.pickle
            # file for future usage
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def upload(self, file_to_upload: Path, folder_id: str):
        filename = file_to_upload.name
        mime_type = 'application/octet-stream'
        body = {'name': filename, 'parents': [folder_id], 'mimeType': mime_type}
        try:
            media_body = MediaFileUpload(file_to_upload, mimetype=mime_type, chunksize=10485760, resumable=True)
            request = self.service.files().create(body=body, media_body=media_body)  # Modified
            result = request.execute()
            return result
        except Exception as e:
            error_message = f'Upload error. Type {e.__class__.__name__} error {e}'
            raise UploadError(error_message)


if __name__ == '__main__':
    sec_file = Path(__file__).parent.parent.parent / '.envs' / 'google_drive' / 'client_secrets.json'
    folder_file = sec_file.parent / 'payjoy_google_folders.json'
    with open(folder_file, 'r') as f:
        folders_dict = json.load(f)
    print(sec_file, sec_file.exists())
    file_to_upload = sec_file.parent.parent.parent / 'README.md'
    print(file_to_upload, file_to_upload.exists())
    upload_folder_id = folders_dict['circulo_tests']  # Circulo tests
    gdrive = GDrive(secrets_file=sec_file)
    response = gdrive.upload(file_to_upload, upload_folder_id)

