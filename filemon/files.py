import os
from PySide import QtGui, QtCore


class FileSystemModel(QtGui.QFileSystemModel):

    filter_reset = QtCore.Signal()
    root_index_changed = QtCore.Signal(QtCore.QModelIndex)

    def __init__(self):
        QtGui.QFileSystemModel.__init__(self)
        self.setFilter(QtCore.QDir.AllDirs |
                       QtCore.QDir.NoDot |
                       QtCore.QDir.NoDotDot |
                       QtCore.QDir.AllEntries |
                       QtCore.QDir.DirsFirst |
                       QtCore.QDir.Name)

    @QtCore.Slot(str)
    def filter_changed(self, text):
        print('filter changed', text)
        # FIXME: doesn't work after root changing
        text = text.strip()
        if text:
            self.setNameFilters(['*'+text+'*'])
        else:
            self.setNameFilters([])
        self.setNameFilterDisables(False)

    def set_path(self, path):
        print(path)
        path = os.path.abspath(path)
        self.setRootPath(path)
        self.filter_reset.emit()
        self.root_index_changed.emit(self.index(path))

    @QtCore.Slot()
    def go_parent(self):
        path = self.rootPath()
        self.set_path(path + '/..')
