#!/usr/bin/env python3


from pathlib import Path
import termcolor
import argparse
from cf_str_literal import bist_stdcpp_h_str, default_cpp_file_str, default_py_file_str
import os

ap = argparse.ArgumentParser("cf")
ap_subparsers = ap.add_subparsers(dest="func", required=True)
ap_init_folder = ap_subparsers.add_parser("init_folder")
ap_init_folder.add_argument("init_folder_path", action="store", type=str)
ap_start = ap_subparsers.add_parser("start")
ap_start.add_argument("--lang", action="store", type=str,
                      default="cpp", choices=["cpp", "py"])
ap_start.add_argument("start_q", action="store", type=str)

anchor_str = "cf"


def check_anchor():
    with open(".anchor", "r") as fp:
        if fp.readline() != anchor_str:
            return
    raise FileNotFoundError(
        "Not find proper anchor, check if you are on root of cf.")


def main_init_folder(init_folder_path: str):
    init_folder_path = Path(init_folder_path)
    init_folder_path.mkdir(exist_ok=True)
    (init_folder_path / "tests").mkdir(exist_ok=True)
    (init_folder_path / "bin").mkdir(exist_ok=True)
    include_bits_folder_path = (init_folder_path / "include" / "bits")
    os.makedirs(include_bits_folder_path)
    with open((include_bits_folder_path / "stdc++.h"), "w") as fp:
        fp.write(bist_stdcpp_h_str)
    with open((init_folder_path / ".anchor"), "w") as fp:
        fp.write(anchor_str)
        fp.write("\n")


def main_start(start_q: str, lang: str):
    check_anchor()
    p = Path.cwd() / f"{start_q}.{lang}"
    if p.exists():
        raise FileExistsError(
            f"Creating existing file {p}, remove it and start then.")
    with open(p, "w") as fp:
        if lang == "cpp":
            fp.write(default_cpp_file_str)
        elif lang == "py":
            fp.write(default_py_file_str)
        else:
            raise ValueError(f"Unsupported to start with lang {lang}")
    # TODO: append info to compile_commands?


if __name__ == '__main__':
    argv = ap.parse_args()
    print(argv)
    if argv.func == 'init_folder':
        main_init_folder(argv.init_folder_path)
    elif argv.func == 'start':
        main_start(argv.start_q, argv.lang)
    else:
        raise ValueError(f"Not supported func {argv.func}")
