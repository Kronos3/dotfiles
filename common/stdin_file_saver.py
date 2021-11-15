import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# Block until stdin is closed
# That way we don't open the dialog immediately
import sys
data = sys.stdin.buffer.read()

dialog = Gtk.FileChooserDialog(
    title="Save file", parent=None, action=Gtk.FileChooserAction.SAVE
)

# Don't allow the window to tile
dialog.set_resizable(False)

dialog.add_buttons(
    Gtk.STOCK_CANCEL,
    Gtk.ResponseType.CANCEL,
    Gtk.STOCK_SAVE,
    Gtk.ResponseType.ACCEPT,
)

response = dialog.run()
if response == Gtk.ResponseType.ACCEPT:
    with open(dialog.get_filename(), "wb+") as f:
        f.write(data)
elif response == Gtk.ResponseType.CANCEL:
    pass

dialog.destroy()
