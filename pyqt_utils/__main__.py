import argparse
import platform
from pathlib import Path
from subprocess import getoutput


def _find_executable(name: str) -> str:
    path = Path()
    if platform.system() == "Windows":
        name = f"{name}.exe"
    for item in path.rglob(name):
        if item.is_file():
            return str(item.resolve())
    raise FileNotFoundError(f"Executable '{name}' not found.")


def main() -> None:
    from pyqt_utils import pyqt_tools_version

    parser = argparse.ArgumentParser(
        prog="pyqt-utils",
        description="Utility scripts for your PyQt project.",
    )

    parser.add_argument(
        "package",
        action="store",
        help="Path to your main python package.",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"PyQt-Utils v{pyqt_tools_version}",
    )

    parser.add_argument(
        "--compile-ui",
        action="store_true",
        dest="compile_ui",
        help="Compile all .ui files in the ui/ directory to .py files.",
    )

    parser.add_argument(
        "--compile-icons",
        action="store_true",
        dest="compile_icons",
        help="Compile the icons/icons.qrc file to a resource.py file.",
    )

    parser.add_argument(
        "--update-langs",
        action="store_true",
        dest="update_langs",
        help="Update all .ts files in the langs/ directory from the .ui and "
        ".py files.",
    )

    parser.add_argument(
        "--lupdate-file",
        action="append",
        dest="lupdate_files",
        help="Additional .py files to include in the lupdate command.",
    )

    parser.add_argument(
        "--compile-langs",
        action="store_true",
        dest="compile_langs",
        help="Compile all .ts files in the langs/ directory to .qm files.",
    )

    parser.set_defaults(func=lambda _: parser.print_help())

    args = parser.parse_args()

    from pyqt_utils import init_app

    init_app("PyQt-Utils", args.package)

    package = Path(args.package).resolve()

    if args.compile_ui:
        for ui_file in package.rglob("ui/*.ui"):
            if not ui_file.is_file():
                continue
            print(
                getoutput(
                    f"{_find_executable("pyuic6")} {ui_file} -o "
                    f"{ui_file.with_suffix('.py').with_stem(
                        ui_file.stem + "_ui"
                    )}"
                ),
                end="",
            )

    if args.compile_icons:
        print(
            getoutput(
                f"rcc --generator python {package}/icons/icons.qrc -o "
                f"{package}/icons/resource.py"
            ),
            end="",
        )
        resource_file = Path(package) / "icons" / "resource.py"
        resource_file.write_text(
            resource_file.read_text("utf-8").replace("PyQt5", "PyQt6"),
            encoding="utf-8",
        )

    if args.update_langs:
        lupdate_files = (
            " ".join(args.lupdate_files) if args.lupdate_files else ""
        )
        print(lupdate_files)
        for ts_file in package.rglob("langs/*.ts"):
            if not ts_file.is_file():
                continue
            print(
                getoutput(
                    f"{_find_executable("lupdate")} -tr-function-alias "
                    f"translate=tr {lupdate_files} {package}/ui/ -ts "
                    f"{ts_file} -no-obsolete -source-language en_US"
                ),
                end="",
            )

    if args.compile_langs:
        for ts_file in package.rglob("langs/*.ts"):
            if not ts_file.is_file():
                continue
            print(
                getoutput(f"{_find_executable("lrelease")} {ts_file}"),
                end="",
            )
