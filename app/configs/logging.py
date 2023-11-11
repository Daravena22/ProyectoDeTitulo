import logging, os, sys
from concurrent_log_handler import ConcurrentRotatingFileHandler
from app.common.env_utils import EnvUtils

logger = logging.getLogger("configs.logging")
this = sys.modules[__name__]
this.handlers = None
DEFAULT_INTERNAL_LEVEL = "INFO"
DEFAULT_INTERNAL_PATH = "data/logs"
DEFAULT_CONSOLE_FORMAT = "%(levelname).3s %(asctime)s.%(msecs)03d | %(name)s => %(message)s"
DEFAULT_CONSOLE_DATE_FORMAT = "%X"
DEFAULT_CONSOLE_COLORLOG_FORMAT = "%(log_color)s%(levelname).3s%(reset)s %(asctime)s.%(msecs)03d | %(name)s %(log_color)s=>%(reset)s %(message)s"
DEFAULT_CONSOLE_COLORLOG_DATE_FORMAT = "%X"
DEFAULT_FILE_FORMAT = "%(levelname).3s %(asctime)s.%(msecs)03d | %(name)s => %(message)s"
DEFAULT_FILE_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class LoggingConfigs:
    
    def init():
        this.handlers = {}
        level = LoggingConfigs.get_level()
        logger_config = logging.getLogger()
        # handler console_colorlog
        handler_console_colorlog = get_handler_console_colorlog()
        if handler_console_colorlog is not None:
            register_handler(logger_config, "console_colorlog", handler_console_colorlog)
        # handler console
        if handler_console_colorlog is None:
            handler_console = get_handler_console()
            register_handler(logger_config, "console", handler_console)
        # handler file
        handler_file = get_handler_file()
        if handler_file is not None:
            register_handler(logger_config, "file", handler_file)
        # set level
        set_level(level, logger_config)
        set_level(3, logging.getLogger("apscheduler"))
        logger.info(f"Logger configurado con nivel {level}")
        logger.info(f"Logger handlers: {list(this.handlers.keys())}")
    
    def get_mode():
        value = EnvUtils.get("LOGGING_MODE") 
        if value is None:
            return ':basic'
        return value

    def get_level():
        value = EnvUtils.get("LOGGING_LEVEL")
        if value is None:
            return 4
        return int(value)
    

def set_level(level: int, logger_config = logging.getLogger()):
    if level <= 1: level = logging.CRITICAL
    elif level == 2: level = logging.ERROR
    elif level == 3: level = logging.WARNING
    elif level == 4: level = logging.INFO
    elif level >= 5: level = logging.DEBUG
    logger_config.setLevel(level)

def register_handler(logger_config: logging.Logger, code:str, handler: logging.Handler):
    logger_config.addHandler(handler)
    this.handlers[code] = len(logger_config.handlers) -1

def get_path():
    value = EnvUtils.get("LOGGING_PATH")
    if value is None:
        value = 'logs'

    value = os.path.normpath(value)
    os.makedirs(value, exist_ok=True)
    value = f"{value}/logging.log"
    value = os.path.normpath(value)
    return value

def get_files_size_limit():
    value = EnvUtils.get("LOGGING_FILES_SIZE_LIMIT")
    if value is None:
        return 2
    value = int(value)
    return value

def get_files_total_limit():
    value = EnvUtils.get("LOGGING_FILES_TOTAL_LIMIT")
    if value is None:
        return 5
    value = int(value)
    return value

def get_handler_console():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        DEFAULT_CONSOLE_FORMAT,
        DEFAULT_CONSOLE_DATE_FORMAT
    ))
    return handler

def get_handler_console_colorlog():
    try:
        from colorlog import ColoredFormatter
    except ModuleNotFoundError:
        return None
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(ColoredFormatter(
        DEFAULT_CONSOLE_COLORLOG_FORMAT,
        DEFAULT_CONSOLE_COLORLOG_DATE_FORMAT,
        reset=True,
        log_colors={
            "DEBUG":    "white",
            "INFO":     "green",
            "WARNING":  "yellow",
            "ERROR":    "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={},
        style="%"
    ))
    return handler

def get_handler_file():
    path = get_path()
    size_limit = get_files_size_limit()
    total_limit = get_files_total_limit()
    if path is None: return None
    handler = ConcurrentRotatingFileHandler(path, "a", 1024*1024 * size_limit, total_limit, "utf-8")
    handler.setFormatter(logging.Formatter(
        DEFAULT_FILE_FORMAT,
        DEFAULT_FILE_DATE_FORMAT
    ))
    return handler