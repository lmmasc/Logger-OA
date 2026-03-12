"""Bootstrap de compatibilidad Qt para la variante legacy.

En la rama moderna no hace nada: si PySide6 esta disponible, se usa tal cual.
En la rama legacy, si PySide6 no esta instalado pero PySide2 si, registra alias
en sys.modules para que el codigo actual siga importando desde PySide6 y recrea
los enums anidados de Qt6 que el proyecto utiliza hoy.
"""

from __future__ import annotations

import importlib
import importlib.util
import os
import sys
import types
from types import SimpleNamespace


def _namespace(**values):
    return SimpleNamespace(**values)


class _NoOpDllDirectoryHandle:
    def __init__(self, path):
        self.path = path

    def close(self):
        return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def _patch_add_dll_directory():
    if getattr(_patch_add_dll_directory, "_done", False):
        return

    add_dll_directory = getattr(os, "add_dll_directory", None)
    if add_dll_directory is None:
        _patch_add_dll_directory._done = True
        return

    def safe_add_dll_directory(path):
        try:
            return add_dll_directory(path)
        except OSError as exc:
            if getattr(exc, "winerror", None) != 127:
                raise

            current_path = os.environ.get("PATH", "")
            path_entries = current_path.split(os.pathsep) if current_path else []
            if path not in path_entries:
                os.environ["PATH"] = path + os.pathsep + current_path if current_path else path
            return _NoOpDllDirectoryHandle(path)

    os.add_dll_directory = safe_add_dll_directory
    _patch_add_dll_directory._done = True


def _prepend_to_path(path):
    if not path or not os.path.isdir(path):
        return

    current_path = os.environ.get("PATH", "")
    path_entries = current_path.split(os.pathsep) if current_path else []
    if path in path_entries:
        return

    os.environ["PATH"] = path + os.pathsep + current_path if current_path else path


def _prime_qt_windows_dll_paths():
    if sys.platform != "win32":
        return

    candidate_dirs = []

    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        candidate_dirs.append(meipass)

    executable_dir = os.path.dirname(getattr(sys, "executable", "") or "")
    if executable_dir:
        candidate_dirs.append(executable_dir)

    for package_name in ("PySide2", "shiboken2"):
        spec = importlib.util.find_spec(package_name)
        if spec and spec.submodule_search_locations:
            for package_dir in spec.submodule_search_locations:
                candidate_dirs.append(package_dir)
                candidate_dirs.append(os.path.dirname(package_dir))

    if meipass:
        candidate_dirs.append(os.path.join(meipass, "PySide2"))
        candidate_dirs.append(os.path.join(meipass, "shiboken2"))

    for candidate_dir in candidate_dirs:
        _prepend_to_path(candidate_dir)


def _patch_qtcore(QtCore):
    original_qt = QtCore.Qt

    class QtProxy:
        AlignmentFlag = _namespace(
            AlignLeft=original_qt.AlignLeft,
            AlignRight=original_qt.AlignRight,
            AlignHCenter=original_qt.AlignHCenter,
            AlignTop=original_qt.AlignTop,
            AlignBottom=original_qt.AlignBottom,
            AlignVCenter=original_qt.AlignVCenter,
            AlignCenter=original_qt.AlignCenter,
        )
        FocusPolicy = _namespace(
            NoFocus=original_qt.NoFocus,
            ClickFocus=original_qt.ClickFocus,
            StrongFocus=original_qt.StrongFocus,
        )
        WindowType = _namespace(Window=original_qt.Window)
        WidgetAttribute = _namespace(WA_DeleteOnClose=original_qt.WA_DeleteOnClose)
        TimeSpec = _namespace(LocalTime=original_qt.LocalTime, UTC=original_qt.UTC)
        KeyboardModifier = _namespace(ControlModifier=original_qt.ControlModifier)
        ScrollBarPolicy = _namespace(
            ScrollBarAlwaysOn=original_qt.ScrollBarAlwaysOn,
            ScrollBarAlwaysOff=original_qt.ScrollBarAlwaysOff,
            ScrollBarAsNeeded=original_qt.ScrollBarAsNeeded,
        )
        ContextMenuPolicy = _namespace(
            CustomContextMenu=original_qt.CustomContextMenu,
        )

        def __getattr__(self, name):
            return getattr(original_qt, name)

    QtCore.Qt = QtProxy()


def _patch_qtwidgets(QtWidgets):
    QApplication = QtWidgets.QApplication
    QDialog = QtWidgets.QDialog
    QMenu = QtWidgets.QMenu
    QMessageBox = QtWidgets.QMessageBox
    QFileDialog = QtWidgets.QFileDialog
    QSizePolicy = QtWidgets.QSizePolicy
    QAbstractItemView = QtWidgets.QAbstractItemView

    for widget_class in (QApplication, QDialog, QMenu, QMessageBox, QFileDialog):
        if not hasattr(widget_class, "exec") and hasattr(widget_class, "exec_"):
            widget_class.exec = widget_class.exec_

    if not hasattr(QMessageBox, "Icon"):
        QMessageBox.Icon = _namespace(
            NoIcon=QMessageBox.NoIcon,
            Question=QMessageBox.Question,
            Information=QMessageBox.Information,
            Warning=QMessageBox.Warning,
            Critical=QMessageBox.Critical,
        )

    if not hasattr(QMessageBox, "StandardButton"):
        QMessageBox.StandardButton = _namespace(
            NoButton=QMessageBox.NoButton,
            Ok=QMessageBox.Ok,
            Cancel=QMessageBox.Cancel,
            Yes=QMessageBox.Yes,
            No=QMessageBox.No,
        )

    if not hasattr(QMessageBox, "ButtonRole"):
        QMessageBox.ButtonRole = _namespace(
            AcceptRole=QMessageBox.AcceptRole,
            RejectRole=QMessageBox.RejectRole,
            YesRole=QMessageBox.YesRole,
            NoRole=QMessageBox.NoRole,
        )

    if not hasattr(QFileDialog, "FileMode"):
        QFileDialog.FileMode = _namespace(
            AnyFile=QFileDialog.AnyFile,
            ExistingFile=QFileDialog.ExistingFile,
            Directory=QFileDialog.Directory,
            ExistingFiles=QFileDialog.ExistingFiles,
        )

    if not hasattr(QSizePolicy, "Policy"):
        QSizePolicy.Policy = _namespace(
            Fixed=QSizePolicy.Fixed,
            Preferred=QSizePolicy.Preferred,
            Expanding=QSizePolicy.Expanding,
        )

    if not hasattr(QAbstractItemView, "EditTrigger"):
        QAbstractItemView.EditTrigger = _namespace(
            NoEditTriggers=QAbstractItemView.NoEditTriggers,
        )


def _patch_qtgui(QtGui, QtWidgets):
    if not hasattr(QtGui, "QAction") and hasattr(QtWidgets, "QAction"):
        QtGui.QAction = QtWidgets.QAction


def _register_pyside6_aliases(QtCore, QtGui, QtWidgets):
    package = types.ModuleType("PySide6")
    package.QtCore = QtCore
    package.QtGui = QtGui
    package.QtWidgets = QtWidgets
    package.__all__ = ["QtCore", "QtGui", "QtWidgets"]

    sys.modules.setdefault("PySide6", package)
    sys.modules["PySide6.QtCore"] = QtCore
    sys.modules["PySide6.QtGui"] = QtGui
    sys.modules["PySide6.QtWidgets"] = QtWidgets


def _register_shiboken_alias():
    try:
        shiboken2 = importlib.import_module("shiboken2")
    except ModuleNotFoundError:
        return

    sys.modules.setdefault("shiboken6", shiboken2)


def _import_legacy_qt_modules():
    try:
        QtCore = importlib.import_module("PySide2.QtCore")
        QtGui = importlib.import_module("PySide2.QtGui")
        QtWidgets = importlib.import_module("PySide2.QtWidgets")
        return QtCore, QtGui, QtWidgets
    except (ImportError, ModuleNotFoundError) as exc:
        raise ImportError(f"No se pudo inicializar PySide2 para la variante legacy: {exc}")


def bootstrap():
    if getattr(bootstrap, "_done", False):
        return

    try:
        importlib.import_module("PySide6.QtCore")
        bootstrap._done = True
        return
    except ModuleNotFoundError:
        pass

    _patch_add_dll_directory()
    _prime_qt_windows_dll_paths()
    QtCore, QtGui, QtWidgets = _import_legacy_qt_modules()

    _patch_qtcore(QtCore)
    _patch_qtwidgets(QtWidgets)
    _patch_qtgui(QtGui, QtWidgets)
    _register_pyside6_aliases(QtCore, QtGui, QtWidgets)
    _register_shiboken_alias()
    bootstrap._done = True