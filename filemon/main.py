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

        self.toolbar = self.addToolBar("Navigation")

        self.main_widget = QtGui.QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.cwd_edit = QtGui.QLineEdit()
        # select_path = QtGui.QPushButton("Go")
        self.filter_edit = QtGui.QLineEdit()

        self.fileBrowserWidget = QtGui.QWidget(self)

        self.filemodel = QtGui.QFileSystemModel()
        self.filemodel.setFilter(QtCore.QDir.AllDirs |
                                 QtCore.QDir.NoDot |
                                 QtCore.QDir.NoDotDot |
                                 QtCore.QDir.AllEntries |
                                 QtCore.QDir.DirsFirst |
                                 QtCore.QDir.Name)

        self.file_view = QtGui.QListView(parent=self)
        self.file_view.setModel(self.filemodel)
        self.file_view.doubleClicked[QtCore.QModelIndex].connect(self.chdir)

        self.selectionModel = self.file_view.selectionModel()
        self.selectionModel.currentChanged.connect(self.do_preview)

        self.preview = QtGui.QLabel(parent=self)
        splitter = QtGui.QSplitter(QtCore.Qt.Vertical, parent=self)
        splitter.addWidget(self.file_view)
        splitter.addWidget(self.preview)

        hbox = QtGui.QVBoxLayout()
        hbox.addWidget(self.cwd_edit)
        hbox.addWidget(self.filter_edit)
        hbox.addWidget(splitter)
        self.main_widget.setLayout(hbox)
        self.setup_toolbar()

    def setup_toolbar(self):
        style = self.style()
        home_icon = style.standardIcon(QtGui.QStyle.SP_DirHomeIcon, None, self)
        home_act = QtGui.QAction(QtGui.QIcon(home_icon),
                                 "&Home", self,
                                 shortcut=QtGui.QKeySequence.Open,
                                 statusTip="Home folder",
                                 triggered=self.do_home_action)
        self.toolbar.addAction(home_act)

        refresh_icon = style.standardIcon(
            QtGui.QStyle.SP_BrowserReload, None, self)
        refresh_act = QtGui.QAction(refresh_icon,
                                    "&Refresh", self,
                                    shortcut=QtGui.QKeySequence.Refresh,
                                    statusTip="Refresh page",
                                    triggered=self.do_refresh_action)
        self.toolbar.addAction(refresh_act)

        back_icon = style.standardIcon(
            QtGui.QStyle.SP_FileDialogToParent, None, self)
        back_act = QtGui.QAction(back_icon, "&Parent", self,
                                 shortcut=QtGui.QKeySequence.Back,
                                 statusTip="Parent directory",
                                 triggered=self.do_back_action)
        self.toolbar.addAction(back_act)

    def do_home_action(self):
        self.set_path(os.path.expanduser('~'))

    def do_refresh_action(self):
        pass

    def do_back_action(self):
        path = self.filemodel.rootPath()
        self.set_path(path + '/..')

    def do_preview(self, new, old):
        fname = self.filemodel.filePath(new)
        image = QtGui.QImage(fname)
        pixmap = QtGui.QPixmap.fromImage(image)
        if not pixmap.isNull():
            size = self.preview.size()
            pixmap = pixmap.scaledToHeight(size.height())
        self.preview.setPixmap(pixmap)

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
