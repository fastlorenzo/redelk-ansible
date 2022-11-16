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
    class ColorFallback():
        __getattr__ = lambda self, name: ''
    Fore = Back = Style = ColorFallback()

def color_diff(diff):
    for line in diff:
        if line.startswith('+'):
            yield Fore.GREEN + line + Fore.RESET
        elif line.startswith('-'):
            yield Fore.RED + line + Fore.RESET
        elif line.startswith('^'):
            yield Fore.BLUE + line + Fore.RESET
        else:
            yield line

def check_redelk_scripts(redelkpath, rolespath, redelkdir, ansiblepath):
    print('Checking RedELK scripts (%s)' % ansiblepath)
    redelk_files = [f for f in os.listdir('%s/%s' % (redelkpath, redelkdir)) if isfile(join('%s/%s' % (redelkpath, redelkdir), f))]

    files = {}
    for rf in redelk_files:
        to_check = '%sredelk-server/files/%s%s' % (rolespath, ansiblepath, rf)
        ftype = None
        #print('Checking if file %s exists' % to_check)
        if os.path.exists(to_check):
            af = to_check
            ftype = 'file'
        else:
            to_check = '%sredelk-server/templates/%s%s.j2' % (rolespath, ansiblepath, rf)
            #print('Checking if file %s exists' % to_check)
            if os.path.exists(to_check):
                af = to_check
                ftype = 'template'

        if ftype is None:
            print('New file not in Ansible redelk-server: %s' % rf)
            files[rf] = {
                'new': True,
                'diff': ''
            }
        else:
            src_file = '%s/%s/%s' % (redelkpath, redelkdir, rf)
            dst_file = '%sredelk-server/%ss/%s%s%s' % (rolespath, ftype, ansiblepath, rf, '.j2' if ftype == 'template' else '')
            print('%s########### [%s] -> [%s]%s' % (Fore.CYAN, src_file, dst_file, Fore.RESET))

            src_data = open(src_file).readlines()
            dst_data = open(dst_file).readlines()

            diff = difflib.unified_diff(dst_data, src_data)
            diff = color_diff(diff)
            diff = ''.join(diff)
            files[rf] = {
                'new': False,
                'diff': diff
            }
            print(diff)

    print('******** Summary for %s ********' % ansiblepath)
    for f in files:
        print('%s%s: %d' % ('+ ' if files[f]['new'] else '', f, len(files[f]['diff'])))
    print('***************************************************\n')

def check_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--redelkpath", metavar="<redelkpath>", dest="redelkpath", default='../../RedELK/', help="Path to RedELK directory (default ../../RedELK/)")
    parser.add_argument("--rolespath", metavar="<rolespath>", dest="rolespath", default='../roles/', help="Path to RedELK roles directory (default ../roles/)")
    parser.add_argument("--client", action='store_true', help="Check client components")
    parser.add_argument("--server", action='store_true', help="Check server components")
    parser.add_argument("--all", action='store_true', help="Check all components (similar to --client --server)")
    args = parser.parse_args()

    if not args.client and not args.server and not args.all:
        print("[-] Missing argument")
        sys.exit(-1)

    return args

if __name__ == '__main__':

    args = check_args()

    redelkpath = args.redelkpath if args.redelkpath else '../../RedELK/'
    rolespath = args.rolespath if args.rolespath else '../roles/'

    check_redelk_scripts(redelkpath, rolespath, 'elkserver/scripts/','usr/share/redelk/bin/')
    check_redelk_scripts(redelkpath, rolespath, 'elkserver/logstash/ruby-scripts/','etc/logstash/ruby-scripts/')
