import os
from pathlib import Path


def symlink(src, dest):
	dest_p = Path(dest).expanduser()
	src_p = Path(src).expanduser()
	
	if dest_p.exists():
		print("Removing old destination %s" % dest)
		os.remove(str(dest_p))
	
	if not dest_p.parent.exists():
		os.system("mkdir -p %s" % dest_p.parent.relative_to("/"))
	
	print("symlinking %s -> %s" % (dest, src))
	os.symlink(src, str(dest_p))


links = {
	"i3.cfg": "~/.config/i3/config",
	"polybar.cfg": "~/.config/polybar/config",
	"Xresources.cfg": "~/.Xresources",
	"fonts": "~/.local/share/fonts",
	"rofi.cfg": "~/.config/rofi/config"
}

for src_raw in links:
	src = os.path.abspath(src_raw)
	symlink(src, links[src_raw])

