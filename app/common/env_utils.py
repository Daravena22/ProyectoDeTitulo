import logging
from os import getenv as os_getenv
from dotenv import load_dotenv

logger = logging.getLogger("main.common.envutils")

PREFIX = "NELLYJOYAS"

class EnvUtils():

    def load_from_file():
        logger.debug("Loading configs from .env file")
        load_dotenv()

    def get(variable):
        logger.debug(f"Get: {variable}")
        value = os_getenv(variable)
        logger.debug(f"Value direct: {value}")
        if value == "": value = None
        if value is not None: return value
        logger.debug(f"Value with prefix ({PREFIX}): {value}")
        value = os_getenv(f"{PREFIX}_{variable}")
        if value == "": value = None
        return value