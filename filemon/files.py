from PySide import QtGui, QtCore


class FileSystemModel(QtGui.QFileSystemModel):

    filter_reset = QtCore.Signal()

    def __init__(self):
        QtGui.QFileSystemModel.__init__(self)
        self.setFilter(QtCore.QDir.AllDirs |
                       QtCore.QDir.NoDot |
                       QtCore.QDir.NoDotDot |
                       QtCore.QDir.AllEntries |
                       QtCore.QDir.DirsFirst |
                       QtCore.QDir.Name)
        self.setNameFilterDisables(False)

    @QtCore.Slot(str)
    def filter_changed(self, text):
        text = text.strip()
        if text:
            self.setNameFilters(['*'+text+'*'])
        else:
            self.setNameFilters([])
