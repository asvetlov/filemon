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

        self.mainWidget = QtGui.QWidget(self)
        self.setCentralWidget(self.mainWidget)

        self.optionsWidget = QtGui.QWidget(self)

        files_list = QtGui.QListWidget()
        select_path_label = QtGui.QLabel("Path")
        dest_path_edit = QtGui.QLineEdit()
        select_path = QtGui.QPushButton("Go")
        description_label = QtGui.QLabel("Description")
        description_edit = QtGui.QLineEdit()
        start = QtGui.QPushButton("Start")

        self.fileBrowserWidget = QtGui.QWidget(self)

        self.filemodel = QtGui.QFileSystemModel()
        self.filemodel.setFilter(QtCore.QDir.Name |
                                 QtCore.QDir.AllDirs |
                                 QtCore.QDir.NoDot |
                                 QtCore.QDir.NoDotDot |
                                 QtCore.QDir.AllEntries |
                                 QtCore.QDir.IgnoreCase |
                                 QtCore.QDir.DirsFirst |
                                 QtCore.QDir.LocaleAware)

        self.file_view = QtGui.QListView(parent=self)
        self.file_view.setModel(self.filemodel)
        self.file_view.doubleClicked[QtCore.QModelIndex].connect(self.chdir)

        self.selectionModel = self.file_view.selectionModel()

        group_input = QtGui.QGroupBox()
        grid_input = QtGui.QGridLayout()

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.file_view)
        self.fileBrowserWidget.setLayout(hbox)

        grid_input.addWidget(select_path_label, 0, 0)
        grid_input.addWidget(dest_path_edit, 1, 0)
        grid_input.addWidget(select_path, 1, 1)
        grid_input.addWidget(description_label, 2, 0)
        grid_input.addWidget(description_edit, 3, 0)
        grid_input.addWidget(start, 3, 1)
        group_input.setLayout(grid_input)

        vbox_options = QtGui.QVBoxLayout(self.optionsWidget)
        vbox_options.addWidget(files_list)
        vbox_options.addWidget(group_input)
        self.optionsWidget.setLayout(vbox_options)

        splitter_filelist = QtGui.QSplitter()
        splitter_filelist.setOrientation(QtCore.Qt.Vertical)
        splitter_filelist.addWidget(self.fileBrowserWidget)
        splitter_filelist.addWidget(self.optionsWidget)
        vbox_main = QtGui.QVBoxLayout(self.mainWidget)
        vbox_main.addWidget(splitter_filelist)
        vbox_main.setContentsMargins(0, 0, 0, 0)
        # self.setLayout(vbox_main)

    def set_path(self, path):
        self.filemodel.setRootPath(path)

    def chdir(self, index):
        # get selected path of folder_view
        index = self.selectionModel.currentIndex()
        if not self.filemodel.isDir(index):
            return
        dir_path = self.filemodel.filePath(index)

        self.filemodel.setRootPath(dir_path)
        self.file_view.setRootIndex(self.filemodel.index(dir_path))


def main():
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    main.set_path(os.getcwd())

    sys.exit(app.exec_())
