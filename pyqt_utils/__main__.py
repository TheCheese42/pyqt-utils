import argparse
import os
import platform
from pathlib import Path
from textwrap import dedent


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

    parser.add_argument(
        "--build-linux",
        action="store_true",
        dest="build_linux",
        help="Build the Linux binary using Nuitka.",
    )

    parser.add_argument(
        "--build-windows",
        action="store_true",
        dest="build_windows",
        help="Build the Windows executable using Nuitka.",
    )

    parser.add_argument(
        "--build-macos",
        action="store_true",
        dest="build_macos",
        help="Build the MacOS binary using Nuitka.",
    )

    parser.add_argument(
        "--build-product-name",
        action="store",
        dest="product_name",
        help="Set the product name for the Nuitka build.",
    )

    parser.add_argument(
        "--build-icon",
        action="store",
        dest="icon_path",
        help="The path to an icon file for the built binary file. Should be "
             "a .png file for Linux and MacOS and a .ico file for Windows.",
    )

    parser.add_argument(
        "--build-data-dir",
        action="append",
        dest="data_dirs",
        help="Add a data dir for the Nuitka build. Uses the format "
             "source=dest.",
    )

    parser.add_argument(
        "--build-data-file",
        action="append",
        dest="data_files",
        help="Add a data file for the Nuitka build. Uses the format "
             "source=dest.",
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
                os.system(
                    f"{_find_executable("pyuic6")} {ui_file} -o "
                    f"{ui_file.with_suffix('.py').with_stem(
                        ui_file.stem + "_ui"
                    )}"
                ),
                end="",
            )

    if args.compile_icons:
        print(
            os.system(
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
                os.system(
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
                os.system(f"{_find_executable("lrelease")} {ts_file}"),
                end="",
            )

    build_command = dedent(
        f"""nuitka \
        --standalone \
        --onefile \
        --python-flag="no_asserts" \
        --python-flag="no_docstrings" \
        --python-flag="-m" \
        --main="{package.name}" \
        --prefer-source-code \
        --output-dir="build/" \
        --enable-plugin=pyqt6 \
        """  # noqa
    )
    if (package / "styles").exists():
        build_command += f"--include-data-dir=\"{package}/styles/=styles/\" "
    if (package / "icons").exists():
        build_command += f"--include-data-dir=\"{package}/icons/=icons/\" "
    if (package / "langs").exists():
        build_command += f"--include-data-dir=\"{package}/langs/=langs/\" "
    if (package / "ui").exists():
        build_command += f"--include-data-dir=\"{package}/ui/=ui/\" "
    if (package / "licenses").exists():
        build_command += f"--include-data-dir=\"{package}/licenses/=licenses/\" "  # noqa
    if (package / "version.txt").exists():
        build_command += f"--include-data-file=\"{package}/version.txt=version.txt\" "  # noqa
        build_command += f"--product-version=\"{(package / "version.txt").read_text("utf-8")}\" "  # noqa
        build_command += f"--file-version=\"{(package / "version.txt").read_text("utf-8")}\" "  # noqa
    if args.product_name:
        build_command += f"--product-name=\"{args.product_name}\" "
    for data_dir in args.data_dirs or []:
        build_command += f"--include-data-dir=\"{data_dir}\" "
    for data_file in args.data_files or []:
        build_command += f"--include-data-file=\"{data_file}\" "

    if args.build_linux:
        command = build_command
        if args.icon_path:
            command += f"--linux-icon=\"{args.icon_path}\" "
        print(os.system(command), end="")

    if args.build_windows:
        command = build_command
        command += "--windows-console-mode=\"attach\" "
        if args.icon_path:
            command += f"--windows-icon-from-ico=\"{args.icon_path}\" "
        print(os.system(command), end="")

    if args.build_macos:
        command = build_command
        if args.product_name:
            command += f"--macos-app-name=\"{args.product_name}\" "
        if args.icon_path:
            command += f"--macos-app-icon=\"{args.icon_path}\" "
        print(os.system(command), end="")
