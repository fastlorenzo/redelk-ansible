#!/bin/env python3
import argparse
import sys
import os
import difflib
from os.path import isfile, join
from pprint import pprint

try:
    from colorama import Fore, Back, Style, init

    init()
except ImportError:  # fallback so that the imported classes always exist

    class ColorFallback:
        def __getattr__(self, name):
            return ""

    Fore = Back = Style = ColorFallback()


def color_diff(diff):
    for line in diff:
        if line.startswith("+"):
            yield Fore.GREEN + line + Fore.RESET
        elif line.startswith("-"):
            yield Fore.RED + line + Fore.RESET
        elif line.startswith("^"):
            yield Fore.BLUE + line + Fore.RESET
        else:
            yield line


def check_redelk_scripts(redelk_path, roles_path, redelk_dir, ansible_path):
    print(f"Checking RedELK scripts ({ansible_path})")
    redelk_files = [
        f
        for f in os.listdir(f"{redelk_path}/{redelk_dir}")
        if isfile(join(f"{redelk_path}/{redelk_dir}", f))
    ]

    files = {}
    for redelk_file in redelk_files:
        to_check = f"{roles_path}redelk-server/files/{ansible_path}{redelk_file}"
        ftype = None
        # print('Checking if file %s exists' % to_check)
        if os.path.exists(to_check):
            af = to_check
            ftype = "file"
        else:
            to_check = (
                f"{roles_path}redelk-server/templates/{ansible_path}{redelk_file}.j2"
            )
            # print('Checking if file %s exists' % to_check)
            if os.path.exists(to_check):
                af = to_check
                ftype = "template"

        if ftype is None:
            print(f"New file not in Ansible redelk-server: {redelk_file}")
            files[redelk_file] = {"new": True, "diff": ""}
        else:
            src_file = f"{redelk_path}/{redelk_dir}/{redelk_file}"
            dst_file = "{rolespath}redelk-server/{ftype}s/{ansiblepath}{redelk_file}{'.j2' if ftype == 'template' else ''}"
            print(f"{Fore.CYAN}########### [{src_file}] -> [{dst_file}]{Fore.RESET}")

            src_data = open(src_file, encoding="utf-8").readlines()
            dst_data = open(dst_file, encoding="utf-8").readlines()

            diff = difflib.unified_diff(dst_data, src_data)
            diff = color_diff(diff)
            diff = "".join(diff)
            files[redelk_file] = {"new": False, "diff": diff}
            print(diff)

    print(f"******** Summary for {ansible_path} ********")
    for f in files:
        print(f'{"+ " if files[f]["new"] else ""}{f}: {len(files[f]["diff"])}')
    print("***************************************************\n")


def check_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "--redelkpath",
        metavar="<redelkpath>",
        dest="redelkpath",
        default="../../RedELK/",
        help="Path to RedELK directory (default ../../RedELK/)",
    )
    parser.add_argument(
        "--rolespath",
        metavar="<rolespath>",
        dest="rolespath",
        default="../roles/",
        help="Path to RedELK roles directory (default ../roles/)",
    )
    parser.add_argument("--client", action="store_true", help="Check client components")
    parser.add_argument("--server", action="store_true", help="Check server components")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Check all components (similar to --client --server)",
    )
    args = parser.parse_args()

    if not args.client and not args.server and not args.all:
        print("[-] Missing argument")
        sys.exit(-1)

    return args


if __name__ == "__main__":

    args = check_args()

    redelkpath = args.redelkpath if args.redelkpath else "../../RedELK/"
    rolespath = args.rolespath if args.rolespath else "../roles/"

    check_redelk_scripts(
        redelkpath, rolespath, "elkserver/scripts/", "usr/share/redelk/bin/"
    )
    check_redelk_scripts(
        redelkpath,
        rolespath,
        "elkserver/logstash/ruby-scripts/",
        "etc/logstash/ruby-scripts/",
    )
