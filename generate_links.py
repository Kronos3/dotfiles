#!/usr/bin/env python3

import argparse
import os
import json
import subprocess

from pathlib import Path
from typing import Dict


def symlink(src: Path, dest: Path, pretend=False):
    dest_p = Path(dest).expanduser().absolute()
    src_p = src.expanduser().absolute()

    if dest_p.exists() or dest_p.is_symlink():
        print("Removing old destination %s" % dest)
        if not pretend:
            os.remove(str(dest_p))

    if not dest_p.parent.exists() and not pretend:
        os.system("mkdir -p %s" % dest_p.parent.relative_to("/"))

    print("symlinking %s -> %s" % (dest, src))
    if not pretend:
        dest_p.parent.mkdir(exist_ok=True, parents=True)
        os.symlink(src_p, str(dest_p))


def get_bool_input(prompt) -> bool:
    while True:
        i = input(prompt).lower()
        if i in ['y', 'yes', 'true']:
            return True
        elif i in ['', 'n', 'no', 'false']:
            return False
        print("Invalid input yes/no true/false")


def parse_config(machine, cfg_path: Path) -> Dict[Path, Path]:
    out: Dict[Path, Path] = {}
    with open(cfg_path) as f:
        j = json.load(f)
        if "import" in j:
            for file in j["import"]:
                out.update(parse_config(machine, file.replace("$MACHINE", machine)))

        if "run" in j:
            for script in j["run"]:
                script = script.replace("$MACHINE", machine)

                if get_bool_input("Run %s? [y/N]: " % script):
                    run_stat = subprocess.run([script], shell=True)
                    if run_stat.returncode != 0:
                        print("%s failed with %s" % (script, run_stat.returncode))
                        exit(1)
                else:
                    print("Skipping script %s" % script)

        if "files" in j:
            for src, dest in j["files"].items():
                out[Path(src.replace("$MACHINE", machine))] = Path(dest.replace("$MACHINE", machine))

    return out


def link_config(cfg: Dict[Path, Path], pretend=False):
    for src, dest in cfg.items():
        symlink(src, dest, pretend=pretend)


def main():
    parser = argparse.ArgumentParser(description="Generate symlinks for a machine configuration")
    parser.add_argument("machine", help="Machine to with configuration (directory)")
    parser.add_argument("--pretend", action="store_true", help="Don't make any filesystem changes, just print stuff")

    args = parser.parse_args()

    machine_p = Path(args.machine)
    if machine_p.exists():
        machine_cfg = parse_config(args.machine,
                                   machine_p / "config.json")
        link_config(machine_cfg, pretend=args.pretend)
    else:
        print("Machine '%s' not found" % args.machine)
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
