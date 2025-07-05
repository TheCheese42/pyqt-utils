import json
import platform
from datetime import datetime
from typing import Any

try:
    from .app_conf import app_name
    from .paths import CONFIG_DIR, CONFIG_PATH, LIB_DIR, LOGGER_PATH
    from .version import version_string
except ImportError:
    from app_conf import app_name  # type: ignore[no-redef]
    from paths import CONFIG_PATH  # type: ignore[no-redef]
    from paths import (  # type: ignore[no-redef]
        CONFIG_DIR,
        LIB_DIR,
        LOGGER_PATH,
    )
    from version import version_string  # type: ignore[no-redef]

_default_config: dict[str, Any] = {}


def config_exists() -> bool:
    return CONFIG_PATH.exists()


def trunc_log() -> None:
    with open(LOGGER_PATH, "w") as fp:
        fp.write("")


def init_config(
    default_config: dict[str, Any],
    create_lib_dir: bool = False,
) -> None:
    """
    Create all necessary directories and files for config, logging and data
    storage.

    :param default_config: A dictionary with all available config keys and
    their default values.
    :type default_config: dict[str, Any]
    :param create_lib_dir: Create the optional lib folder, useful for generated
    or downloaded files that do not need to be in a possibly synched config
    folder, defaults to False
    :type create_lib_dir: bool, optional
    """
    global _default_config
    log(f"{app_name} - Version {version_string}")
    log(f"Running on {platform.platform()}")
    _default_config = default_config
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if create_lib_dir:
        LIB_DIR.mkdir(parents=True, exist_ok=True)
    trunc_log()

    if not config_exists():
        with open(CONFIG_PATH, "w", encoding="utf-8") as fp:
            json.dump(default_config, fp)


def _get_config() -> dict[str, Any]:
    with open(CONFIG_PATH, "r", encoding="utf-8") as fp:
        text = fp.read()
    try:
        conf: dict[str, Any] = json.loads(text)
    except json.JSONDecodeError as e:
        log(f"Failed to decode configuration file: {e}", "ERROR")
        log("Creating new config")
        conf = _default_config
    for key in conf.copy():
        if key not in _default_config:
            del conf[key]
    for key in _default_config:
        if key not in conf:
            conf[key] = _default_config[key]
    return conf


def _overwrite_config(config: dict[str, Any]) -> None:
    try:
        text = json.dumps(config)
    except Exception as e:
        log(f"Failed to dump configuration: {e}", "ERROR")
        return
    with open(CONFIG_PATH, "w", encoding="utf-8") as fp:
        fp.write(text)


def get_config_value(key: str) -> Any:
    try:
        val = _get_config()[key]
    except KeyError:
        val = _default_config[key]
    return val


def set_config_value(key: str, value: Any) -> None:
    config = _get_config()
    config[key] = value
    _overwrite_config(config)


def log(msg: str, level: str = "INFO") -> None:
    time = datetime.now().isoformat()
    with open(LOGGER_PATH, "a", encoding="utf-8") as fp:
        fp.write(f"[{time}] [{level}] {msg}\n")


class LogStream:
    def __init__(self, level: str = "INFO") -> None:
        self.level = level

    def write(self, text: str) -> None:
        log(text, self.level)
