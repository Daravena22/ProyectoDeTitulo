import logging
from app.common.env_utils import EnvUtils

logger = logging.getLogger("main.configs.database")

DEFAULT_DATABASE_PORTS = {
    "postgresql": 5432,
    "mysql+pymysql": 3306
}

class DatabaseConfigs:

    def get_uri():
        try:
            engine = get_engine()
            if engine not in ("postgresql", "mysql+pymysql"):
                raise Exception(f"Database engine not recognized: {engine}")
            uri = "{}://{}:{}@{}:{}/{}".format(
                engine,
                get_user(),
                get_password(),
                get_host(),
                get_port(),
                get_catalog()
            )
            return uri
        except Exception as ex:
            raise Exception(f"Error reading DATABASE configs: {str(ex)}")

def get_user():
    value = EnvUtils.get("DATABASE_USER")
    if value is None:
        raise Exception("Error getting DATABASE_USER, configure it using environment variables")
    logger.info("DATABASE_USER = [LOADED]")
    return value

def get_password():
    value = EnvUtils.get("DATABASE_PASSWORD")
    if value is None:
        raise Exception("Error getting DATABASE_PASSWORD, configure it using environment variables")
    logger.info("DATABASE_PASSWORD = [LOADED]")
    return value

def get_engine():
    value = EnvUtils.get("DATABASE_ENGINE")
    if value is None:
        raise Exception("Error getting DATABASE_ENGINE, configure it using environment variables")
    if value == "postgres": value = "postgresql"
    elif value == "mysql": value = "mysql+pymysql"
    if value not in ["postgresql", "mysql+pymysql"]:
        raise Exception(f"Invalid DATABASE_ENGINE: {value}")
    logger.info(f"DATABASE_ENGINE = {value}")
    return value

def get_host():
    value = EnvUtils.get("DATABASE_HOST")
    if value is None:
        raise Exception("Error getting DATABASE_HOST, configure it using environment variables")
    logger.info("DATABASE_HOST = [LOADED]")
    return value

def get_port():
    value = EnvUtils.get("DATABASE_PORT")
    if value is None:
        engine = get_engine()
        if engine == "postgresql": value = DEFAULT_DATABASE_PORTS["postgresql"]
        elif engine == "mysql+pymysql": value = DEFAULT_DATABASE_PORTS["mysql+pymysql"]
        if value is None:
            raise Exception("Error getting DATABASE_PORT [DEFAULT], invalid engine")
        logger.info(f"DATABASE_PORT [DEFAULT] = {value}")
        return value
    try:
        value = int(value)
    except Exception as ex:
        raise Exception(f"Error getting DATABASE_PORT: {str(ex)}")
    logger.info(f"DATABASE_PORT = {value}")
    return value

def get_catalog():
    value = value = EnvUtils.get("DATABASE_CATALOG")
    if value is None:
        raise Exception("Error getting DATABASE_CATALOG, configure it using environment variables")
    logger.info("DATABASE_CATALOG = [LOADED]")
    return value