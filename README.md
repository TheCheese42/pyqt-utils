# PyQt-Utils

A set of classes and tools providing basic functionality useful in PyQt applications.

## Initialization

Before importing anything else you must initialize PyQt-Utils.

```py
from pyqt_utils import init_app

init_app("AppName", __file__)
```

## Version

PyQt-Utils helps with version management. To define the project version, create a version.txt in your package folder.

```text
1.0.0
```

Now you can import the version module:

```py
from pyqt_utils.version import __version__, version_string

print(f"{__version__} | {version_string}")
# (1, 0, 0) | 1.0.0
```

### Bump the Version

To increase the version number, use the bump_version.py script that was installed to your virtual environment.

```sh
python bump_version.py <package> --major
python bump_version.py <package> --minor
python bump_version.py <package> --patch
```

`<package>` must be replaced with the path to the python package containing the `version.txt` file.

If available, the `pyproject.toml` and `Product.wxs` will be updated as well.

## Paths and Config

The following paths can be imported from the `pyqt_utils.paths` module:

- `ROOT_PATH` - The path to the main python package
- `VERSION_PATH` - The path to the `version.txt` file
- `STYLE_PATH` - The path to the `styles/` directory (optional)
- `ICONS_PATH` - The path to the `icons/` directory (optional)
- `LANGS_PATH` - The path to the `langs/` directory (optional)
- `LICENSES_PATH` - The path to the `licenses/` directory (optional)
- `CONFIG_DIR` - The path to the platform-dependant settings and app data directory. For more details see `AppDataLocation` in the [PySide docs](https://doc.qt.io/qtforpython-6/PySide6/QtCore/QStandardPaths.html)
- `LIB_DIR` - The path to the platform-dependant directory for storing files that shouldn't be transferred over different systems. See `AppLocalDataLocation` (Windows) or `HomeLocation` (Other) in the [PySide docs](https://doc.qt.io/qtforpython-6/PySide6/QtCore/QStandardPaths.html)
- `CONFIG_PATH` - The path to the `config.json` file. Usually not accessed directly.
- `LOGGER_PATH` - The path to the `latest.log` file. Usually not accessed directly.

To use the built-in config, import the config module:

```py
from pyqt_utils import config

default_config = {
    "show_welcome_message": True,
    "example_setting": 42,
}

# pass `create_lib_dir = True` if you want to use the LIB_DIR path.
config.init_config(default_config)

config.set_config_value("show_welcome_message", False)
print(config.get_config_value("show_welcome_message"))
# False
```

The config will be saved automatically every time something is changed.

## Styles

Your `styles/` directory should look like this:

```txt
styles/
├── style_group
│   ├── dark
│   │   └── stylesheet.qss
│   ├── light
│   │   └── stylesheet.qss
```

Groups of styles are within one folder, each `.qss` file is within its own folder.
The folder names will be used as display names.

```py
from pyqt_utils.styles import find_styles

print(find_styles())
# {"style_group": [
#     Style(name="style_group dark", stylesheet="..."),
#     Style(name="style_group light", stylesheet="..."),
# ]}
```

You can add those to a QMenu or a QComboBox.

## Licenses

Your `licenses/` directory should look like this:

```txt
licenses/
├── python.json
├── python.txt
├── pyqt6.json
├── pyqt6.txt
```

```json
// python.json
{
    "name": "Python",
    "content_file": "python.txt",
    "link": "https://www.python.org",
}
```

The `python.txt` file will contain the raw license text.

```py
from pyqt_utils.licenses import find_licenses

print(find_licenses())
# [
#     License(name="Python", content="...", link="https://www.python.org"),
#     License(name="PyQt6", ...),
# ]
```

You can also directly generate a nice dialog for viewing all licenses:

```py
from pyqt_utils.licenses import LicenseViewer

# From within your main window
def open_licenses() -> None:
    license_viewer = LicenseViewer(self)
    license_viewer.exec()
```

## Scripts

All script except for bump_version.py must be run from the main package directory.
Every shell script has a bash and a PowerShell version, only the file extension changes from `.sh` to `.ps1`.
The following scripts were installed to your virtual environment:

- bump_version.py (see section "Version")
- compile-ui.sh - Compile all `.ui` files in the `ui/` directory
- compile-icons.sh - Compile all icons from the `icons/` directory into the `icons/resource.py` resource file
- compile-langs.sh - Compile all `.ts` files from the `langs/` directory into `.qm` files.
