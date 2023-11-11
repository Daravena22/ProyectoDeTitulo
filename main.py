from app import app
from app.configs.app import AppConfigs

if (__name__) == "__main__":
    app.run(AppConfigs.get_host(), AppConfigs.get_port(), AppConfigs.get_debug())

