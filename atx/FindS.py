"""
    findS
    ~~~~~~~~~~~~

    FindS is a tool for search keywords in a path.

    Author: tkorays
    Datatime: 2017-12-8
"""
import os
import re
import sys
import click
import tkinter as tk
import tkinter.ttk as ttk


class FileFilter:
    def __init__(self):
        pass

    def filt(self, p):
        pass


def log_v(verbose, str):
    if verbose:
        print(str)


def find_str_in_file(strs, file_path, verbose=False):
    if isinstance(strs, list) or isinstance(strs, tuple):
        result = {k: [] for k in strs}
    else:
        result = {strs: []}

    ln = 0
    with open(file_path, 'r') as f:
        for line in f:
            ln += 1
            for k in result.keys():
                if re.search(k, line):
                    log_v(verbose, "Find keyword '{}' in {}: line {}".format(k, os.path.abspath(file_path), ln))
                    result[k].append(ln)
    return result


def find_file_in_path(start, filters=[], recurse=True):
    result = []
    start = os.path.abspath(start)

    if os.path.isfile(start) and os.path.exists(start):
        return [start, ]

    if not os.path.isdir(start) or not os.path.exists(start):
        return []

    files = os.listdir(start)
    for f in files:
        f = os.path.join(start, f)
        if os.path.isfile(f):
            filter_result = True
            for ft in filters:
                filter_result = True if ft.filt(f) else False
            if filter_result:
                result.append(f)
        elif os.path.isdir(f) and recurse:
            result.extend(find_file_in_path(f, filters, recurse))

    return result


class FindS:
    def __init__(self, filters=None, recurse=True, verbose=False):
        self.filters = filters if filters else []
        self.result = {}
        self.recurse = recurse
        self.verbose = verbose

    def find(self, strs, paths):
        files = []
        if isinstance(paths, list) or isinstance(paths, tuple):
            for p in paths:
                if not isinstance(p, str):
                    continue
                files.extend(find_file_in_path(p, filters=self.filters, recurse=self.recurse))
        elif isinstance(paths, str):
            files.extend(find_file_in_path(paths, filters=self.filters, recurse=self.recurse))

        for f in files:
            r = find_str_in_file(strs, f, self.verbose)
            for v in r.values():
                if v:
                    self.result[f] = r
                    break

    def save_to_file(self, fn):
        with open(fn, 'w') as f:
            for sf in self.result.keys():
                for keyword in self.result[sf].keys():
                    for line in self.result[sf][keyword]:
                        f.write('Find keyword "{}" in "{}": line {}\n'.format(keyword, sf, line))


class ExtensionFilter(FileFilter):
    def __init__(self, exts):
        super().__init__()
        self.exts = [exts, ] if isinstance(exts, str) else exts

    def filt(self, p):
        return os.path.splitext(p)[1] in self.exts


@click.command()
@click.version_option("v1.0.0")
@click.option('--strs', help='Strings for searching, e.g. "abc,efg,aaa"')
@click.option('--path', help="Start search files in the path.")
@click.option('--extensions', help="Extensions for searching files, e.g. '.h,.c,.cpp'")
@click.option('--recurse', type=int, default=1, help="Search recursively or not.")
@click.option('--log', default='', help="Result file path.")
@click.option('--verbose', type=int, default=0, help="Show details when processing.")
def command_line_for_FindS(strs, path, extensions, recurse, log, verbose):
    ft = [ExtensionFilter(extensions.split(',')), ] if extensions else []
    fs = FindS(filters=ft, recurse=True if recurse else False, verbose=True if verbose else False)
    fs.find(strs.split(','), path)
    if log:
        fs.save_to_file(log)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("GUI")
    else:
        # command line
        command_line_for_FindS()
