import os
from PySide import QtGui, QtCore


class FileSystemModel(QtGui.QFileSystemModel):

    filter_reset = QtCore.Signal()
    root_index_changed = QtCore.Signal(QtCore.QModelIndex)
    status_changed = QtCore.Signal(int, int)

    STORAGE_NAME = '.filemon.dat'

    def __init__(self):
        QtGui.QFileSystemModel.__init__(self)
        self.setFilter(QtCore.QDir.AllDirs |
                       QtCore.QDir.NoDot |
                       QtCore.QDir.NoDotDot |
                       QtCore.QDir.AllEntries |
                       QtCore.QDir.DirsFirst |
                       QtCore.QDir.Name)

        self._processed = set()
        self._total_count = 0
        self.setNameFilterDisables(False)

    @QtCore.Slot(str)
    def filter_changed(self, text):
        print('filter changed', text)
        text = text.strip()
        if text:
            self.setNameFilters(['*' + text + '*'])
        else:
            self.setNameFilters([])

    def set_path(self, path):
        print(path)
        path = os.path.abspath(path)
        self.reset()
        self.setRootPath(path)
        self.filter_reset.emit()
        self.root_index_changed.emit(self.index(path))
        storage = os.path.join(path, self.STORAGE_NAME)
        self._processed = set()
        present = set(os.listdir(path))
        self._total_count = sum(1 for i in present if not i.startswith('.'))
        if os.path.isfile(storage):
            with open(storage) as f:
                data = set(f.read().splitlines())
            self._processed = data - present
            if data != self._processed:
                self._save()
        self.status_changed.emit(self._total_count, len(self._processed))

    @QtCore.Slot()
    def go_parent(self):
        path = self.rootPath()
        self.set_path(path + '/..')

    @QtCore.Slot()
    def go_home(self):
        path = os.path.expanduser('~')
        self.set_path(path)

    @QtCore.Slot()
    def go_cwd(self):
        self.set_path(os.getcwd())

    def file_dragged(self, path):
        print("Dragged", path)
        self._processed.add(path)
        self._save()

    def _save(self):
        self.status_changed.emit(self._total_count, len(self._processed))
        storage = os.path.join(self.rootPath(), self.STORAGE_NAME)
        with open(storage, 'w') as f:
            f.write('\n'.join(sorted(self._processed)))

    def data(self, index, role):
        if index.isValid() and role == QtCore.Qt.ForegroundRole:
            path = self.filePath(index)
            if path in self._processed:
                return QtGui.QBrush(QtGui.QColor(255, 0, 0))
        return super().data(index, role)

    @QtCore.Slot()
    def reset_markers(self):
        self._processed = set()
        self._save()
        self.set_path(self.rootPath())

    def unmark(self, index):
        if not index.isValid():
            return
        path = self.filePath(index)
        self._processed.discard(path)
        self._save()
        self.set_path(self.rootPath())


class FileView(QtGui.QListView):

    def __init__(self, parent):
        QtGui.QListView.__init__(self, parent)
        self.setDragEnabled(True)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._drag_start_pos = event.pos()
        return QtGui.QListView.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        if not event.buttons() & QtCore.Qt.LeftButton:
            return
        if ((event.pos() - self._drag_start_pos).manhattanLength() <
                QtGui.QApplication.startDragDistance()):
            return

        model = self.model()
        drag = QtGui.QDrag(self)
        index = self.indexAt(self._drag_start_pos)
        if not index.isValid():
            return
        if model.isDir(index):
            return
        path = model.filePath(index)

        mimedata = model.mimeData([index])

        drag.setMimeData(mimedata)

        drop_action = drag.exec_(QtCore.Qt.CopyAction)
        if drop_action == QtCore.Qt.CopyAction:
            model.file_dragged(path)
