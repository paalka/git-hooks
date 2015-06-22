#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, print_function
import os
import subprocess
import sys


def system(*args, **kwargs):
    """
    Executes a subprocess by creaing a child process.
    Returns the output from the process as a string.
    """

    kwargs.setdefault('stdout', subprocess.PIPE)
    proc = subprocess.Popen(args, **kwargs)
    out, err = proc.communicate()
    return out


def find_modified_files():
    """
    Finds the filename of all files currently staged that have been added,
    modified, copied. Returns a list of the filenames of the modified files.
    """

    modified_files = system('git', 'diff', '--cached', '--name-only',
                            '--diff-filter=ACM').split()
    return modified_files


def filter_files(filenames):
    """
    Pair the file extension of a file with the filename. Returns a dict where
    the file extension is the key, and the filenames are contained in a list.
    """

    file_dict = {}
    for filename in filenames:
        file_extension = os.path.splitext(filename)[1][1:]

        if file_dict.get(file_extension):
            file_dict[file_extension].append(filename)
        else:
            file_dict[file_extension] = [filename]

    return file_dict


def validate_python(filename):
    """
    Ensures that the given file 'filename' conforms to the pep8 standard.
    Returns True/False depending on whether the file is valid or not.
    """

    errors = system('pep8', filename).strip()

    if errors:
        print(errors)

    return errors == ''


def validate_files(files_dict):
    """
    Validates several different files depending on their file type.
    Exits with 0/1 as the status depending on whether
    the all files are valid or not.
    """

    VALIDATION_FUNCTION = {"py": validate_python}

    IS_VALID = {True: 0, False: 1}
    all_valid = True

    for extension, files in files_dict.items():
        # Get the validation function for the specific filetype
        validation_func = VALIDATION_FUNCTION.get(extension)

        if validation_func:
            for filename in files:
                print("\nValidating " + filename + "...")
                file_is_valid = validation_func(filename)

                if file_is_valid:
                    print(filename + " is valid!\n")
                else:
                    all_valid = False

    sys.exit(IS_VALID[all_valid])


if __name__ == '__main__':
    modified_files = find_modified_files()
    files_dict = filter_files(modified_files)

    validate_files(files_dict)
