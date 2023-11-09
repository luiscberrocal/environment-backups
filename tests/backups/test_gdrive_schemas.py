from environment_backups.backups.gdrive_schemas import Installed


class TestGoogleConfiguration:

    def test_create_minimal(self):
        installed_app = Installed(client_id='jjjjjj',
                                  project_id='my-new-project',
                                  client_secret='jjjjsdfas')
        assert installed_app
