import sys
from PySide import QtGui, QtCore
import os


class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.resize(600, 600)
        self.setWindowTitle('FileMon')
        exit = QtGui.QAction('Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit from program')
        self.connect(exit,
                     QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        self.statusBar()
        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(exit)

        self.main_widget = QtGui.QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.cwd_edit = QtGui.QLineEdit()
        # select_path = QtGui.QPushButton("Go")
        self.filter_edit = QtGui.QLineEdit()

        self.fileBrowserWidget = QtGui.QWidget(self)

        self.filemodel = QtGui.QFileSystemModel()
        self.filemodel.setFilter(QtCore.QDir.AllDirs |
                                 QtCore.QDir.NoDot |
                                 # QtCore.QDir.NoDotDot |
                                 QtCore.QDir.AllEntries |
                                 QtCore.QDir.DirsFirst |
                                 QtCore.QDir.Name)

        self.file_view = QtGui.QListView(parent=self)
        self.file_view.setModel(self.filemodel)
        self.file_view.doubleClicked[QtCore.QModelIndex].connect(self.chdir)

        self.selectionModel = self.file_view.selectionModel()

        hbox = QtGui.QVBoxLayout()
        hbox.addWidget(self.cwd_edit)
        hbox.addWidget(self.filter_edit)
        hbox.addWidget(self.file_view)
        self.main_widget.setLayout(hbox)

    def set_path(self, path):
        print(path)
        path = os.path.abspath(path)
        self.filemodel.setRootPath(path)
        self.file_view.setRootIndex(self.filemodel.index(path))
        if self.cwd_edit.text != path:
            self.cwd_edit.setText(path)

    def chdir(self, index):
        # get selected path of folder_view
        index = self.selectionModel.currentIndex()
        if not self.filemodel.isDir(index):
            return
        dir_path = self.filemodel.filePath(index)
        self.set_path(dir_path)


def main():
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    main.set_path(os.getcwd())

    sys.exit(app.exec_())
