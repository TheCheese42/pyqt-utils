#!/usr/bin/env python3

import argparse
import re
import sys
from pathlib import Path

V = "1.0.0"

PYPROJECT_PATH = Path() / "pyproject.toml"
PRODUCT_WXS_PATH = Path() / "Product.wxs"


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="version-bumper",
        description="Bump the version number. Sets the version for all files "
        "containing a version number, including version.txt, "
        "pyproject.toml and the Windows installer script.",
    )

    parser.add_argument(
        "package",
        action="store",
        help="Path to the python package whose version should be bumped.",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"bump_version.py v{V}",
    )
    parser.set_defaults(func=lambda _: parser.print_help())

    parser.add_argument(
        "--major",
        action="store_true",
        required=False,
        default=False,
        dest="major",
        help="Increase the major version.",
    )
    parser.add_argument(
        "--minor",
        action="store_true",
        required=False,
        default=False,
        dest="minor",
        help="Increase the minor version.",
    )
    parser.add_argument(
        "--patch",
        action="store_true",
        required=False,
        default=False,
        dest="patch",
        help="Increase the patch version.",
    )

    args = parser.parse_args()

    version_path = Path(args.package) / "version.txt"
    if not version_path.exists():
        print(
            f"Version file {version_path} does not exist. "
            "Please create a version.txt file with the current version."
        )
        sys.exit(1)
    version_string = version_path.read_text(encoding="utf-8").strip()
    __version__: tuple[int, ...] = tuple(map(int, version_string.split(".")))

    to_modify: tuple[bool, bool, bool] = (args.major, args.minor, args.patch)
    if sum(to_modify) > 1:
        print("You mustn't specify more than 1 version option.")
        sys.exit(1)
    new_version: list[int] = list(__version__)
    if to_modify[0]:
        new_version[0] += 1
        new_version[1] = 0
        new_version[2] = 0
    elif to_modify[1]:
        new_version[1] += 1
        new_version[2] = 0
    elif to_modify[2]:
        new_version[2] += 1
    new_tuple: tuple[int, ...] = tuple(new_version)
    if new_tuple == __version__:
        parser.print_help()
        sys.exit(0)
    new_string = ".".join(map(str, new_tuple))

    version_path.write_text(new_string, encoding="utf-8")

    if PYPROJECT_PATH.exists():
        pyproject_text = PYPROJECT_PATH.read_text(encoding="utf-8")
        if match := re.search(r"version = \"([\d\.]*)\"", pyproject_text):
            start = match.start(1)
            pyproject_list = list(pyproject_text)
            del pyproject_list[start : match.end(1)]
            for i, char in enumerate(new_string):
                pyproject_list.insert(start + i, char)
            PYPROJECT_PATH.write_text(
                "".join(pyproject_list), encoding="utf-8"
            )
            print("Updated pyproject.toml version.")

    if PRODUCT_WXS_PATH.exists():
        product_wxs_text = PRODUCT_WXS_PATH.read_text(encoding="utf-8")
        if match := re.search(r"Version=\"([\d\.]*)\"", product_wxs_text):
            start = match.start(1)
            product_wxs_list = list(product_wxs_text)
            del product_wxs_list[start : match.end(1)]
            for i, char in enumerate(new_string):
                product_wxs_list.insert(start + i, char)
            PRODUCT_WXS_PATH.write_text(
                "".join(product_wxs_list), encoding="utf-8"
            )
            print("Updated Product.wxs version.")

    print(f"Set Version to {new_string}")


if __name__ == "__main__":
    main()
