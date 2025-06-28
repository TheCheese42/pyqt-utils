try:
    from .paths import VERSION_PATH
except ImportError:
    from paths import VERSION_PATH  # type: ignore[no-redef]

version_string = VERSION_PATH.read_text(encoding="utf-8").strip()
__version__: tuple[int, ...] = tuple(map(int, version_string.split(".")))
