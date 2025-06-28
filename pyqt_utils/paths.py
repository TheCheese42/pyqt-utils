import platform
from pathlib import Path

from PyQt6.QtCore import QStandardPaths

try:
    from .app_conf import app_name, root_file
except ImportError:
    from app_conf import app_name, root_file  # type: ignore[no-redef]

if not app_name:
    raise RuntimeError(
        "The application name must be set before importing the paths module. "
        "Use `pyqt_utils.init_app(...)`."
    )
if not root_file:
    raise RuntimeError(
        "The application root file must be set before importing the paths "
        "module. Use `pyqt_utils.init_app(...)`."
    )

ROOT_PATH = Path(root_file).parent
if "__compiled__" in globals():
    # With nuitka, __file__ will show the file in a subfolder that doesn't
    # exist.
    # With nuitka: app_name.dist/app_name/paths.py
    # Actual: app_name.dist/paths.py
    # That's why we go back another folder using .parent twice.
    ROOT_PATH = Path(root_file).parent.parent
VERSION_PATH = ROOT_PATH / "version.txt"
STYLES_PATH = ROOT_PATH / "styles"
ICONS_PATH = ROOT_PATH / "icons"
LANGS_PATH = ROOT_PATH / "langs"
LICENSES_PATH = ROOT_PATH / "licenses"

CONFIG_DIR = (
    Path(
        QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppDataLocation
        )
    )
    / app_name
)

if platform.system() == "Windows":
    LIB_DIR = (
        Path(
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.AppLocalDataLocation
            )
        )
        / app_name
        / "lib"
    )
else:
    LIB_DIR = (
        Path(
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.HomeLocation
            )
        )
        / f".{app_name}"
        / "lib"
    )
CONFIG_PATH = CONFIG_DIR / "config.json"
LOGGER_PATH = CONFIG_DIR / "latest.log"
