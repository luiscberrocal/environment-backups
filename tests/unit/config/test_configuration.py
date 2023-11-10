from environment_backups.config.configuration import ConfigurationManager


class TestConfigurationManager:

    def test_init(self, tmp_config_folder):
        configuration = ConfigurationManager(tmp_config_folder)
        assert not configuration.config_file.exists()

    def test_import_from_json(self, tmp_config_folder, fixtures_folder):
        config_json_file = fixtures_folder / 'app_configuration.json'

        configuration = ConfigurationManager(tmp_config_folder)

        config_data = configuration.import_from_json(config_json_file).get_current()

        assert configuration.config_file.exists()
        assert config_data




