import json
from typing import NamedTuple

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

try:
    from .paths import LICENSES_PATH
    from .utils import open_url
except ImportError:
    from paths import LICENSES_PATH  # type: ignore[no-redef]
    from utils import open_url  # type: ignore[no-redef]


class License(NamedTuple):
    name: str
    content: str
    link: str


def find_licenses() -> list[License]:
    """
    Find all licenses in the licenses directory.

    :return: A dictionary of license names and their content and link.
    :rtype: dict[str, str]
    """
    licenses: list[License] = []
    for item in sorted(LICENSES_PATH.iterdir()):
        if item.is_file() and item.suffix == ".json":
            meta = json.loads(item.read_text(encoding="utf-8"))
            name = str(meta.get("name", None))
            if name is None:
                raise ValueError(f"License file {item} has no name.")
            content_file = str(meta.get("content_file", None))
            if content_file is None:
                raise ValueError(f"License file {item} has no content_file.")
            content = (item.parent / content_file).read_text(encoding="utf-8")
            link = str(meta.get("link", ""))
            licenses.append(License(name=name, content=content, link=link))
    return sorted(licenses, key=lambda x: x.name)


class LicenseViewer(QDialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.licenses = find_licenses()
        self.double_tap_hint = "{link}"
        self.setupUi()
        self.connectSignalsSlots()
        self.retranslateUi()
        self.setup_licenses()

    def setupUi(self) -> None:
        self.setWindowTitle("Licenses")
        self.resize(730, 410)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title = QLabel(self)
        self.title.setObjectName("title")
        font = QFont()
        font.setPointSize(18)
        self.title.setFont(font)

        self.verticalLayout.addWidget(
            self.title, 0, Qt.AlignmentFlag.AlignHCenter
        )
        self.verticalSpacer = QSpacerItem(
            20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed
        )
        self.verticalLayout.addItem(self.verticalSpacer)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.list = QListWidget(self)
        self.list.setObjectName("list")
        self.list.setMaximumSize(QSize(200, 16777215))
        self.list.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.list.setProperty("showDropIndicator", False)
        self.horizontalLayout_2.addWidget(self.list)
        self.line_2 = QFrame(self)
        self.line_2.setObjectName("line_2")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.horizontalLayout_2.addWidget(self.line_2)
        self.browser = QTextBrowser()
        self.browser.setObjectName("browser")
        self.horizontalLayout_2.addWidget(self.browser)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalSpacer_2 = QSpacerItem(
            20, 4, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed
        )
        self.verticalLayout.addItem(self.verticalSpacer_2)
        self.closeBtn = QPushButton()
        self.closeBtn.setObjectName("closeBtn")
        self.verticalLayout.addWidget(self.closeBtn)
        self.closeBtn.clicked.connect(self.close)

    def connectSignalsSlots(self) -> None:
        self.list.itemSelectionChanged.connect(self.show_license)
        self.list.itemDoubleClicked.connect(self.double_clicked)

    def show_license(self) -> None:
        try:
            selected = self.list.selectedItems()[0]
        except IndexError:
            return
        for license in self.licenses:
            if license.name == selected.text():
                self.browser.setText(license.content)
                return

    def double_clicked(self, item: QListWidgetItem) -> None:
        for license in self.licenses:
            if license.name == item.text():
                open_url(license.link)

    def retranslateUi(self) -> None:
        """Override this method if you need localization support."""
        self.title.setText("Licenses")
        self.closeBtn.setText("Close")
        self.double_tap_hint = "{link} (Double tap to open)"

    def setup_licenses(self) -> None:
        self.list.clear()
        for license in self.licenses:
            item = QListWidgetItem(license.name)
            item.setToolTip(self.double_tap_hint.format(link=license.link))
            self.list.addItem(item)
