#!/usr/bin/env python3

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
	dest_p.parent.mkdir(exist_ok=True, parents=True)
	os.symlink(src, str(dest_p))


links = {
	"i3.cfg": "~/.config/i3/config",
	"compton.cfg": "~/.config/compton.conf",
	"polybar.cfg": "~/.config/polybar/config",
	"rofi.cfg": "~/.config/rofi/config",
	"Xresources.cfg": "~/.Xresources",
<<<<<<< HEAD
	"fonts": "~/.local/share/fonts",
	"rofi.cfg": "~/.config/rofi/config"
=======
        "sound-control.sh": "~/.config/polybar/scripts/pulseaudio-control.bash",
	"fonts": "~/.local/share/fonts"
>>>>>>> origin/kronos
}

for src_raw in links:
	src = os.path.abspath(src_raw)
	symlink(src, links[src_raw])

