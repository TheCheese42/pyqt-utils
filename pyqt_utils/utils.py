import platform
import webbrowser
from pathlib import Path
from subprocess import getoutput
from threading import Thread

try:
    from . import config
except ImportError:
    import config  # type: ignore[no-redef]


def open_url(url: str) -> None:
    thread = Thread(target=_open_url_threaded, args=(url,))
    config.log(f"Opening url {url} in thread {thread.name}", "DEBUG")
    thread.start()


def _open_url_threaded(url: str) -> None:
    try:
        webbrowser.WindowsDefault().open(url)  # type: ignore[attr-defined]
    except Exception:
        system = platform.system()
        if system == "Windows":
            getoutput(f"start {url}")
        else:
            getoutput(f"open {url}")


def open_file(path: str | Path) -> None:
    thread = Thread(target=_open_file_threaded, args=(path,))
    config.log(f"Opening file at path {path} in thread {thread.name}", "DEBUG")
    thread.start()


def _open_file_threaded(path: str | Path) -> None:
    try:
        # Webbrowser module can well be used to open regular file as well.
        # The system will use the default application, for the file type,
        # not necessarily the webbrowser.
        webbrowser.WindowsDefault().open(str(path))  # type: ignore[attr-defined]  # noqa
    except Exception:
        system = platform.system()
        if system == "Windows":
            getoutput(f"start {path}")
        else:
            getoutput(f"open {path}")
