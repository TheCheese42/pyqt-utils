from typing import NamedTuple

try:
    from .paths import STYLES_PATH
except ImportError:
    from paths import STYLES_PATH  # type: ignore[no-redef]


class Style(NamedTuple):
    name: str
    stylesheet: str


def find_styles() -> dict[str, list[Style]]:
    """
    Recursively find all styles in the styles directory.

    :return: A list of all styles and (sub-)categories of styles.
    :rtype: list[Style | list[Style]]
    """
    styles: dict[str, list[Style]] = {}
    for item in sorted(STYLES_PATH.iterdir()):
        if item.is_dir():
            group_name = item.name
            styles[group_name] = []
            for sub_theme in sorted(item.iterdir()):
                if sub_theme.is_file() or "cache" in sub_theme.name:
                    continue
                theme_name = sub_theme.name.replace("-", " ").title()
                style = Style(
                    name=f"{group_name.title()} {theme_name}",
                    stylesheet=(sub_theme / "stylesheet.qss").read_text(
                        encoding="utf-8"
                    ),
                )
                styles[group_name].append(style)
    return styles
