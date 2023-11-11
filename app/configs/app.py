import logging, os
from app.common.env_utils import EnvUtils
from app.common.text_utils import TextUtils


logger = logging.getLogger("main.configs.app")

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 5001
DEFAULT_DEBUG = False

class AppConfigs:

    def get_secret_key():
        value = EnvUtils.get("SECRET_KEY")
        if value is None:
            value = TextUtils.generate_random_string(64)
            logger.info("SECRET_KEY [DEFAULT] = [AUTOGENERATED]")
            return value
        logger.info("SECRET_KEY = [LOADED]")
        return value
        
    def get_host():
        value = EnvUtils.get("HOST")
        if value is None:
            value = DEFAULT_HOST
            logger.info(f"HOST [DEFAULT] = {value}")
            return value
        logger.info(f"HOST = {value}")
        return value
    
    def get_port():
        value = EnvUtils.get("PORT")
        if value is None:
            value = DEFAULT_PORT
            logger.info(f"HOST [DEFAULT] = {value}")
            return value
        try:
            value = int(value)
        except Exception as ex:
            raise Exception(f"Error getting PORT: {str(ex)}")
        logger.info(f"PORT = {value}")
        return value

    def get_debug():
        value = EnvUtils.get("DEBUG")
        if value is None:
            value = DEFAULT_DEBUG
            logger.info(f"DEBUG [DEFAULT] = {value}")
            return value
        if value.lower().lstrip().rstrip() == "true": value = True
        elif value.lower().lstrip().rstrip() == "false": value = False
        if type(value) != bool:
            raise Exception("Error getting DEBUG: invalid convertion to boolean")
        logger.info(f"DEBUG = {value}")
        return value
    
