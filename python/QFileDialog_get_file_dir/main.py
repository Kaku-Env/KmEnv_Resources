import sys
import os

from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class FileDialog(QtWidgets.QFileDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
        self.setFileMode(QtWidgets.QFileDialog.AnyFile)

        self.btn_open = self.get_open_btn() # 開くボタン
        self.btn_open.clicked.connect(self.on_open_btn_clicked)

        for widget in (QtWidgets.QListView, QtWidgets.QTreeView):
            children = self.findChildren(widget)
            if children:
                for view in children:
                    view.doubleClicked.connect(self.on_item_double_clicked)
    
    def on_item_double_clicked(self, index):
        """ダブルクリック時の処理"""
        model = self.sender().model()
        file_path = model.filePath(index)
        if os.path.isdir(file_path):
            return
        self.selectFile(file_path)
        self.accept()
    
    def on_open_btn_clicked(self):
        """開くボタンが押された時の処理"""
        selected_file = self.selectedFiles()[0]
        if os.path.isdir(selected_file):
            self.setFileMode(QtWidgets.QFileDialog.Directory)
        self.accept()

    def get_open_btn(self):
        """開くボタンを取得"""
        btn_box = self.findChild(QtWidgets.QDialogButtonBox)
        if btn_box:
            for btn in btn_box.buttons():
                if btn_box.buttonRole(
                    btn) == QtWidgets.QDialogButtonBox.AcceptRole:
                    return btn
        return None
    
    def get_path(self) -> str:
        """エクスプローラーを起動し、選択されたファイル・ディレクトリパスを返す"""
        if self.exec() == QtWidgets.QFileDialog.Accepted:
            return self.selectedFiles()[0]
        else:
            return ""


class ScrollAreaApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scroll Area Example")
        self.setGeometry(100, 100, 400, 300)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)

        # ボタン
        self.add_button = QtWidgets.QPushButton("Add Path")
        self.add_button.clicked.connect(self.add_path)
        self.main_layout.addWidget(self.add_button)

        # スクロールエリア
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)
        self.scroll_content = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)

    def add_path(self):
        """エクスプローラーを起動し、選択されたファイル・ディレクトリパスを
        スクロールエリアに追加"""
        file_dialog = FileDialog(self)
        file_path = file_dialog.get_path()
        if file_path:
            label = QtWidgets.QLabel(file_path)
            label.setAlignment(Qt.AlignLeft)
            self.scroll_layout.addWidget(label)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ScrollAreaApp()
    window.show()
    sys.exit(app.exec())
