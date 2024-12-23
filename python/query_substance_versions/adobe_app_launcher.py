import sys
import winreg

from PySide6 import QtWidgets


ROOT_KEY = "Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall"
GUID_DICT = {}

with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, ROOT_KEY) as key:
    for i in range(winreg.QueryInfoKey(key)[0]): # サブキーの数でループ
        key_name = winreg.EnumKey(key, i)
        # サブキーを開く
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            "{}\\{}".format(ROOT_KEY, key_name)) as subkey:
            value_dict = {} # 値の名前とデータのペアを格納
            for j in range(winreg.QueryInfoKey(subkey)[1]): # 値の数でループ
                curr_value = winreg.EnumValue(subkey, j)
                value_dict[curr_value[0]] = curr_value[1]
        
        GUID_DICT[key_name] = value_dict

def get_adobe_apps_versions() -> dict:
    version_dict = {}
    for v in GUID_DICT.values():
        if "DisplayName" in v.keys():
            if "Photoshop" in v["DisplayName"]:
                version_dict["Photoshop"] = v["DisplayVersion"]
            elif "Substance 3D Painter" in v["DisplayName"]:
                version_dict["Substance 3D Painter"] = v["DisplayVersion"]
            elif "Substance 3D Designer" in v["DisplayName"]:
                version_dict["Substance 3D Designer"] = v["DisplayVersion"]
    return version_dict

class AppLauncher(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.version_dict = get_adobe_apps_versions()
        self.setWindowTitle("AdobeAppLauncher")
        self.setMinimumWidth(400)
        self.setMinimumHeight(200)
        self._init_ui()
    
    def _init_ui(self):
        self.main_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_grid = QtWidgets.QGridLayout()
        self.main_widget.setLayout(self.main_grid)

        # Photoshop
        self.main_grid.addWidget(QtWidgets.QLabel("Photoshop"), 0, 0)
        self.main_grid.addWidget(QtWidgets.QLabel(
            self.version_dict["Photoshop"]), 0, 1)
        self.main_grid.addWidget(QtWidgets.QPushButton("Launch"), 0, 2)
        # Substance Painter
        self.main_grid.addWidget(QtWidgets.QLabel("Substance Painter"), 1, 0)
        self.main_grid.addWidget(QtWidgets.QLabel(
            self.version_dict["Substance 3D Painter"]), 1, 1)
        self.main_grid.addWidget(QtWidgets.QPushButton("Launch"), 1, 2)
        # Substance Designer
        self.main_grid.addWidget(QtWidgets.QLabel("Substance Designer"), 2, 0)
        self.main_grid.addWidget(QtWidgets.QLabel(
            self.version_dict["Substance 3D Designer"]), 2, 1)
        self.main_grid.addWidget(QtWidgets.QPushButton("Launch"), 2, 2)

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    win = AppLauncher()
    win.show()
    app.exec()
    sys.exit()