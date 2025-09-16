from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from interface_adapters.ui.main_window import MainWindow


def find_main_window(widget) -> "MainWindow | None":
    parent = widget.parent()
    while parent:
        if parent.__class__.__name__ == "MainWindow":
            return cast("MainWindow", parent)
        parent = parent.parent()
    return None
