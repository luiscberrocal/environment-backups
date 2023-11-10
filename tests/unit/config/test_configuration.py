from environment_backups.config.configuration import ConfigurationManager


class TestConfigurationManager:

    def test_init(self, output_folder):
        configuration = ConfigurationManager(output_folder)
        assert not configuration.config_file.exists()
