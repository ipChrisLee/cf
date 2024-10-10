#!/usr/bin/env python3


from pathlib import Path
import termcolor
import argparse
from cf_str_literal import (
    bist_stdcpp_h_str,
    default_cpp_file_str,
    default_py_file_str,
    default_clangd_file_str,
    anchor_str,
    default_cmakelists_str,
)
import os
import typing as typ
import subprocess
from subprocess import CalledProcessError, TimeoutExpired
from datetime import datetime
import yaml
import json
import termcolor

ap = argparse.ArgumentParser("cf")
ap_subparsers = ap.add_subparsers(dest="func", required=True)
# cf.py init_folder
ap_init_folder = ap_subparsers.add_parser("init_folder")
ap_init_folder.add_argument("init_folder_path", action="store", type=str)
# cf.py start A --lang cpp --t_limit 1.5
ap_start = ap_subparsers.add_parser("start")
ap_start.add_argument(
    "--lang", action="store", type=str, default="cpp", choices=["cpp", "py"]
)
ap_start.add_argument("--t_limit", action="store", type=float, default=1)
ap_start.add_argument("start_q", action="store", type=str)
# cf.py build A
ap_build = ap_subparsers.add_parser("build")
ap_build.add_argument("build_q", action="store", type=str, default="*")
# cf.py run A
ap_run = ap_subparsers.add_parser("run")
ap_run.add_argument("run_q", action="store", type=str)
# cf.py test_all A
ap_test_all = ap_subparsers.add_parser("test_all")
ap_test_all.add_argument("test_all_q", action="store", type=str)
# cf.py test -t 0 A
ap_test = ap_subparsers.add_parser("test")
ap_test.add_argument("test_q", action="store", type=str)
ap_test.add_argument("-t", dest="test_case", action="store", type=str)
# cf.py new_test A
ap_new_test = ap_subparsers.add_parser("new_test")
ap_new_test.add_argument("new_test_q", action="store", type=str)


def check_anchor():
    with open(".anchor", "r") as fp:
        if fp.readline() != anchor_str:
            return
    raise FileNotFoundError(
        "Not find proper anchor, check if you are on root of cf.")


def do_cmake_configure():
    with open(Path.cwd() / ".cf.yaml", "r") as fp:
        d = yaml.safe_load(fp)
        build_type = d["_build_type"]
    subprocess.run(
        ["cmake", "-S", ".", "-B", "build", "-D",
            f"CMAKE_BUILD_TYPE={build_type}"],
        check=True,
    )


def main_build(build_q: str):
    check_anchor()
    if (Path.cwd() / f"{build_q}.cpp").exists():
        subprocess.run(["cmake", "--build", "build",
                       "--target", build_q], check=True)
    else:
        pass


def main_init_folder(init_folder_path: str):
    init_folder_path = Path(init_folder_path)
    init_folder_path.mkdir(exist_ok=True)
    # root/tests
    (init_folder_path / "tests").mkdir(exist_ok=True)
    # root/include/bits/stdc++.h
    include_bits_folder_path = init_folder_path / "include" / "bits"
    os.makedirs(include_bits_folder_path)
    with open((include_bits_folder_path / "stdc++.h"), "w") as fp:
        fp.write(bist_stdcpp_h_str)
    # root/.anchor
    with open((init_folder_path / ".anchor"), "w") as fp:
        fp.write(anchor_str)
        fp.write("\n")
    # root/.cf.yaml
    with open((init_folder_path / ".cf.yaml"), "w") as fp:
        d = {
            "_create_date": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "_build_type": "Release",
            "_editor": os.environ.get("EDITOR", "nano"),
        }
        yaml.dump(d, fp)
    # root/CMakeLists.txt
    with open((init_folder_path / "CMakeLists.txt"), "w") as fp:
        fp.write(default_cmakelists_str)
    # root/.clangd
    with open((init_folder_path / ".clangd"), "w") as fp:
        fp.write(default_clangd_file_str)


def main_start(start_q: str, lang: str, t_limit: float):
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
    with open(Path.cwd() / ".cf.yaml", "r") as fp:
        d: typ.Dict = yaml.safe_load(fp)
        d.setdefault(start_q, dict())
        d[start_q].setdefault("t_limit", t_limit)
    with open(Path.cwd() / ".cf.yaml", "w") as fp:
        yaml.dump(d, fp)
    do_cmake_configure()
    (Path.cwd() / "tests" / start_q).mkdir(exist_ok=True)


def get_run_command(q: str):
    check_anchor()
    if (Path.cwd() / f"{q}.cpp").exists():
        return [Path.cwd() / "build" / q]
    else:
        return ["python3", f"{q}.py"]


def main_run(run_q: str):
    check_anchor()
    main_build(run_q)
    run_command = get_run_command(q=run_q)
    subprocess.run(run_command, check=True)


def do_test_without_build(test_q: str, t_limit: float, dirpath: Path, test_case: str):
    in_path = Path(dirpath) / f"{test_case}.in"
    out_path = Path(dirpath) / f"{test_case}.out"
    ans_path = Path(dirpath) / f"{test_case}.ans"
    termcolor.cprint(f"Running test case {{{test_case}}}...", color="yellow")
    in_stream = open(in_path, "r")
    ans_stream = open(ans_path, "w")
    run_command = get_run_command(q=test_q)
    fail_reason = ""
    try:
        subprocess.run(
            run_command,
            stdin=in_stream,
            stdout=ans_stream,
            check=True,
            timeout=t_limit,
        )
    except TimeoutExpired as timeout_expired:
        fail_reason = "TLE"
    except CalledProcessError as called_process_error:
        fail_reason = "RE"
    finally:
        in_stream.close()
        ans_stream.close()
    if len(fail_reason) == 0:
        diff_path = "diff"
        # hack for macOS
        if Path("/opt/homebrew/bin/diff").exists():
            diff_path = "/opt/homebrew/bin/diff"
        r = subprocess.run([diff_path, "-Z", "-B", "-q", out_path, ans_path])
        if r.returncode != 0:
            fail_reason = "WA"
    if len(fail_reason) == 0:
        termcolor.cprint("AC", color="green")
    else:
        termcolor.cprint(fail_reason, color="red")


def main_test(test_q: str, test_case: str):
    check_anchor()
    main_build(test_q)
    with open(Path.cwd() / ".cf.yaml", "r") as fp:
        d = yaml.safe_load(fp)
        t_limit = d[test_q]["t_limit"]
    dirpath = Path.cwd() / "tests" / test_q
    do_test_without_build(
        test_q=test_q, t_limit=t_limit, dirpath=dirpath, test_case=test_case
    )


def main_test_all(test_q: str):
    check_anchor()
    main_build(test_q)
    with open(Path.cwd() / ".cf.yaml", "r") as fp:
        d = yaml.safe_load(fp)
        t_limit = d[test_q]["t_limit"]
    for dirpath, dirnames, filenames in os.walk(Path.cwd() / "tests" / test_q):
        dirpath = Path(dirpath)
        test_cases = set()
        for filename in filenames:
            filename = Path(filename)
            test_cases.add(filename.stem)
        for test_case in test_cases:
            do_test_without_build(
                test_q=test_q, t_limit=t_limit, dirpath=dirpath, test_case=test_case
            )


def helper_mex(s: typ.Set[int]) -> int:
    mex_value = len(s)
    for i in range(len(s)):
        if i not in s:
            mex_value = i
            break
    return mex_value


def main_new_test(new_test_q: str):
    check_anchor()
    with open(Path.cwd() / ".cf.yaml", "r") as fp:
        d = yaml.safe_load(fp)
        editor = d["_editor"]
    si = set()
    for dirpath, dirnames, filenames in os.walk(Path.cwd() / "tests" / new_test_q):
        for filename in filenames:
            filename = Path(filename)
            try:
                si.add(int(filename.stem))
            except ValueError:
                pass
    new_test_case_id = helper_mex(si)
    in_file_path = Path.cwd() / "tests" / new_test_q / f"{new_test_case_id}.in"
    out_file_path = Path.cwd() / "tests" / new_test_q / \
        f"{new_test_case_id}.out"
    subprocess.run([editor, in_file_path, out_file_path], check=True)


if __name__ == "__main__":
    argv = ap.parse_args()
    # print(argv)
    if argv.func == "init_folder":
        main_init_folder(argv.init_folder_path)
    elif argv.func == "start":
        main_start(start_q=argv.start_q, lang=argv.lang, t_limit=argv.t_limit)
    elif argv.func == "build":
        main_build(build_q=argv.build_q)
    elif argv.func == "run":
        main_run(run_q=argv.run_q)
    elif argv.func == "test_all":
        main_test_all(test_q=argv.test_all_q)
    elif argv.func == "test":
        main_test(test_q=argv.test_q, test_case=argv.test_case)
    elif argv.func == "new_test":
        main_new_test(new_test_q=argv.new_test_q)
    else:
        raise ValueError(f"Not supported func {argv.func}")
