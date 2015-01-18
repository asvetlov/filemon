import sys
from PySide import QtGui, QtCore

from .files import FileSystemModel, FileView


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

        self.filemodel = FileSystemModel()

        self.cwd_edit = QtGui.QLineEdit()
        self.filemodel.rootPathChanged.connect(self.cwd_edit.setText)
        # select_path = QtGui.QPushButton("Go")
        self.filter_edit = QtGui.QLineEdit()
        self.filter_edit.textChanged.connect(self.filemodel.filter_changed)
        self.filemodel.filter_reset.connect(self.filter_edit.clear)

        self.fileBrowserWidget = QtGui.QWidget(self)

        self.file_view = FileView(parent=self)
        self.file_view.setModel(self.filemodel)
        self.file_view.doubleClicked[QtCore.QModelIndex].connect(self.chdir)
        self.filemodel.root_index_changed.connect(self.file_view.setRootIndex)

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
        self.setup_statusbar()

    def setup_toolbar(self):
        style = self.style()
        home_icon = style.standardIcon(QtGui.QStyle.SP_DirHomeIcon, None, self)
        home_act = QtGui.QAction(QtGui.QIcon(home_icon),
                                 "&Home", self,
                                 shortcut=QtGui.QKeySequence.Open,
                                 statusTip="Home folder",
                                 triggered=self.filemodel.go_home)
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
                                 triggered=self.filemodel.go_parent)
        self.toolbar.addAction(back_act)

        pin_icon = style.standardIcon(
            QtGui.QStyle.SP_DialogYesButton, None, self)
        pin_act = QtGui.QAction(pin_icon, "&Stay on Top", self,
                                shortcut=QtGui.QKeySequence.Back,
                                statusTip="Stay on Top")
        pin_act.toggled.connect(self.do_stay_on_top)
        pin_act.setCheckable(True)
        self.toolbar.addAction(pin_act)

        reset_icon = style.standardIcon(QtGui.QStyle.SP_DialogResetButton,
                                        None, self)
        reset_act = QtGui.QAction(QtGui.QIcon(reset_icon),
                                  "&Reset markers", self,
                                  shortcut=QtGui.QKeySequence.Open,
                                  statusTip="Reset markers",
                                  triggered=self.filemodel.reset_markers)
        self.toolbar.addAction(reset_act)

        unmark_icon = style.standardIcon(QtGui.QStyle.SP_TrashIcon,
                                         None, self)
        unmark_act = QtGui.QAction(QtGui.QIcon(unmark_icon),
                                   "&Unmark the current file", self,
                                   shortcut=QtGui.QKeySequence.Open,
                                   statusTip="Unmark the current file",
                                   triggered=self.unmark_current)
        self.toolbar.addAction(unmark_act)

    def setup_statusbar(self):
        bar = self.statusBar()
        self.counter = QtGui.QLabel(self)
        bar.addWidget(self.counter)
        self.filemodel.status_changed.connect(self.do_update_counter)

    def do_update_counter(self, total, marked):
        print('Update counters')
        txt = "Total: {}, Marked: {}".format(total, marked)
        self.counter.setText(txt)

    def do_refresh_action(self):
        pass

    def do_stay_on_top(self, checked):
        if sys.platform != 'win32':
            return
        flags = self.windowFlags()
        flag = QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.CustomizeWindowHint
        if checked:
            self.setWindowFlags(flags | flag)
        else:
            self.setWindowFlags(flags & ~flag)

    def do_preview(self, new, old):
        fname = self.filemodel.filePath(new)
        image = QtGui.QImage(fname)
        pixmap = QtGui.QPixmap.fromImage(image)
        if not pixmap.isNull():
            size = self.preview.size()
            pixmap = pixmap.scaledToHeight(size.height())
        self.preview.setPixmap(pixmap)

    def chdir(self, index):
        # get selected path of folder_view
        index = self.selectionModel.currentIndex()
        if not self.filemodel.isDir(index):
            return
        dir_path = self.filemodel.filePath(index)
        self.filemodel.set_path(dir_path)

    def unmark_current(self):
        # get selected path of folder_view
        index = self.selectionModel.currentIndex()
        self.filemodel.unmark(index)


def main():
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    main.filemodel.go_cwd()

    sys.exit(app.exec_())
