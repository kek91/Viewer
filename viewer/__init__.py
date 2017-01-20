from fman import DirectoryPaneCommand, show_alert, show_status_message
import os
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class ViewerWindow(QWidget):
    def __init__(self, parent=None):
        super(ViewerWindow, self).__init__(parent)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

class ViewFile(DirectoryPaneCommand):
    def __call__(self):
        file_name = self.pane.get_file_under_cursor()

        if not os.path.isdir(file_name):

            text_edit = QPlainTextEdit()
            # disable text editing
            text_edit.setReadOnly(True)

            # set background color
            palette = QPalette()
            bgcolor = QColor(39, 40, 34)
            palette.setColor(QPalette.Base, bgcolor)
            textc = QColor(200, 200, 200)
            palette.setColor(QPalette.Text, textc)
            text_edit.setPalette(palette)

            # load text file into viewer
            file = QFile(file_name)
            file.open(QFile.ReadOnly)
            text = file.readAll()
            try:
                text = str(text, encoding='utf8')
            except:
                text = str(text)
            text_edit.setPlainText(text)

            global window # FIXME: keep reference to window in app scope

            window = ViewerWindow()
            window.resize(640, 480)
            #window.move(300, 300)
            window.setWindowTitle('Viewer - ' + file_name)

            # add text_edit to qwidget
            window.layout = QVBoxLayout(window)
            window.layout.setContentsMargins(0, 0, 0, 0)
            window.layout.addWidget(text_edit)

            # TODO: display status bar with file type, encoding, length, end line type, wrapping mode

            finfo = os.stat(file_name)
            fsize = finfo.st_size
            fsize = str(int(fsize/1024))+' KB' if int(fsize/1024)>0 else str(int(fsize))+' B'
            flm = datetime.date.fromtimestamp(finfo.st_mtime)
            text_statusbar = os.path.basename(file_name) + " \t - \t " + fsize + " \t - \t " + str(flm)
            # text_statusbar = os.path.basename(file_name) + " \t\t\t " + str(int(fsize / 1024)) + " KB \t\t\t " + str(flm)

            status_bar = QStatusBar()
            status_bar.showMessage(text_statusbar, 0)

            window.layout.addWidget(status_bar)

            window.show()
