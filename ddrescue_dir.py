#!/usr/bin/python3

import os
import sys
import shutil
import argparse
import subprocess

def parse_args():
    examples = '''example usage:
    rescue directory /mnt/data and save it to /home/user/data:
        ./ddrescue_dir.py /mnt/data/ /home/user/
    rescue same directory, but retry reading failed sectors 10 times:
        ./ddrescue_dir.py /mnt/data/ /home/user/ --options="-r 10"'''
    parser = argparse.ArgumentParser(description='ddrescue directory - by /robex/', epilog=examples, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-n', help='dry-run: dont copy files, only show commands', action='store_true')
    parser.add_argument('-i', help='interactive: ask for confirmation for each file', action='store_true')
    parser.add_argument('-v', help='verbose ddrescue mode', action='store_true')
    parser.add_argument('-q', help='quiet: dont display ddrescue output', action='store_true')
    parser.add_argument('--no-log', help='do not store log files (use only if you know what you are doing!)', action='store_true')
    parser.add_argument('--no-scrape', help='skip the scraping phase', action='store_true')
    parser.add_argument('--no-trim', help='skip the trimming phase', action='store_true')
    parser.add_argument('src_dir', help='source directory')
    parser.add_argument('dst_dir', help='destination directory (source folder created automatically)')
    parser.add_argument('--ddpath', help='path to ddrescue binary (only needed if not in $PATH)', default='ddrescue', type=str)
    parser.add_argument('--options', help='any other options to be passed to ddrescue (see example below)', type=str)

    args = parser.parse_args()
    return args

def __main__():
    args = parse_args()
    if not os.path.isdir(args.src_dir):
        print('source directory does not exist, aborting...')
        return
    if not os.path.isdir(args.dst_dir):
        print('destination directory does not exist, aborting...')
        return
    if shutil.which(args.ddpath) is None:
        print('ddrescue binary not found, aborting...')
        return

    rescue_dir(args)


def rescue_dir(args):
    src_dir = os.path.normpath(args.src_dir)
    dst_dir = os.path.normpath(args.dst_dir)

    root_dir = os.path.basename(src_dir)
    dst_dir = os.path.join(dst_dir, root_dir)

    for root, dirs, files in os.walk(src_dir):
        cur_dir = os.path.join(dst_dir, root[len(src_dir)+1:])

        if not args.n:
            if not os.path.isdir(cur_dir):
                os.mkdir(cur_dir)
            else:
                print('folder ' + cur_dir + ' already exists, aborting...')
                return

        for f in files:
            old_path = os.path.join(root, f)
            new_path = os.path.join(cur_dir, f)
            log_path = new_path + '.log'
            arglist = [args.ddpath, old_path, new_path]
            if not args.no_log:
                arglist.append(log_path)
            if args.v:
                arglist.append('-vv')
            if args.q:
                arglist.append('-q')
            if args.i:
                arglist.append('--ask')
            if args.no_scrape:
                arglist.append('--no-scrape')
            if args.no_trim:
                arglist.append('--no-trim')
            if args.options is not None:
                arglist.append(args.options)
            if args.n:
                for arg in arglist:
                    print(arg + ' ', end='')
                print()
            else:
                subprocess.run(arglist)


__main__()
