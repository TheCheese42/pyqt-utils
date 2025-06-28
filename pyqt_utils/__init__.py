try:
    from . import app_conf
except ImportError:
    import app_conf  # type: ignore[no-redef]


def init_app(name: str, root_file: str) -> None:
    """
    Provide information required by pyqt-utils modules.
    This function must be called before import the config or paths modules.

    :param name: The name, must conform to file system rules.
    :type name: str
    :param root_file: The contents of the __file__ variable from a script
    within the main package.
    :type root_file: str
    """
    app_conf.app_name = name
    app_conf.root_file = root_file


pyqt_tools_version = "1.0.0"


__all__ = [
    "init_app",
    "pyqt_tools_version",
]
