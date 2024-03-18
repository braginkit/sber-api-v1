
import pathlib
import yaml

CONFIG_DIR = pathlib.Path(__file__).parent
CONFIG_PATH = CONFIG_DIR / 'config.yaml'


def setup_config(app):
    with open(CONFIG_PATH) as config_file:
        app.config = yaml.full_load(config_file)
