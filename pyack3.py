#!/usr/bin/env python3

# pyack.py but threaded

import re
import sys
import threading
import os
from collections import namedtuple
from queue import Queue

FilepathRegex = namedtuple("FilepathRegex", ["file_path", "regex"])

FILTERING_READ_LIMIT = 1000000
VCS_IGNORE_DIR_NAMES = [".git", ".hg"]
IGNORE_REGEX_PATTERS = ["\\.swp$", "~$", "\\.(png|ico|gif)$", "\\.(pbc|gz)$"]
IGNORE_FILEPATHS = {"string_cs.t", "POD2HTML.pm"}


def file_filter(filter_regex, filter_queue, search_queue):
    """
    Take FilePathRegex objects from filter_queue and put matches into search_queue, finally
    send search_queue None to signal no more objects are coming.

    Args:
        filter_regex <re.compile>: Compiled regex to use for matching against incoming objects.
        filter_queue <Queue[Optional[FilepathRegex]]>: Pick-up queue for potential files.
        search_queue <Queue[Optional[FilepathRegex]]>:
            Queue used to work on objects that pass this filter.
    """
    ignore_regexes = [re.compile(pattern) for pattern in IGNORE_REGEX_PATTERS]
    should_ignore = lambda filepath: filepath in IGNORE_FILEPATHS or next(
        (True for ignore_regex in ignore_regexes if ignore_regex.search(filepath)), False
    )
    next_file_path_regex = filter_queue.get()

    while next_file_path_regex is not None:
        file_path = next_file_path_regex.file_path

        if not should_ignore(file_path):
            # Put our file in the queue, rather than calling findhits
            with open(file_path, "r", encoding="ISO8859") as file:
                if filter_regex.search(file.read(FILTERING_READ_LIMIT)):
                    search_queue.put(FilepathRegex(file_path, next_file_path_regex.regex))

        next_file_path_regex = filter_queue.get()

    search_queue.put(None)


def print_hits_in_file(search_queue):
    """
    Take FilePathRegex objects from search_queue and search the files for matching lines.

    Args:
        search_queue <Queue[Optional[FilepathRegex]]>: Pick-up queue for files.

    Note:
        Used for side-effects, prints results
    """
    next_file_path_regex = search_queue.get()

    while next_file_path_regex is not None:
        file_path = next_file_path_regex.file_path

        with open(file_path, "r", encoding="ISO8859") as file:
            for count, line in enumerate(file):
                if next_file_path_regex.regex.search(line):
                    print(f"{file_path}:{count}:{line.rstrip()}")

        next_file_path_regex = search_queue.get()


def walk_sorted_files(root_directory):
    """
    Walk a root directory in lexicographic order, ignoring top-level git and mercurial metadata

    Args:
        root_directory <str>: path to directory to traverse

    Yields:
        filepath <str>
    """
    ignore_vcs_dirs = {
        os.path.join(root_directory, bottom_level) for bottom_level in VCS_IGNORE_DIR_NAMES
    }
    # directories_impure is used internally by walk, clearing it allows us to short-circuit
    # ignore any children of a directory we dont want to process. Similarly, sorting it allows us to
    # walk the child nodes of the current directory in a lexicographically sorted order.
    for root_node, directories_impure, filenames in os.walk(root_directory):
        if root_node in ignore_vcs_dirs:
            directories_impure[:] = []
            continue
        directories_impure.sort()

        for file_name in sorted(filenames):
            yield os.path.join(root_node, file_name)


def main():
    search_queue = Queue()
    filter_queue = Queue()

    root_directory = sys.argv[2]
    search_regex = re.compile(sys.argv[1])
    filter_regex = re.compile(sys.argv[1], re.M | re.S)

    filter_thread = threading.Thread(
        target=file_filter, args=(filter_regex, filter_queue, search_queue)
    )
    search_thread = threading.Thread(target=print_hits_in_file, args=(search_queue,))
    filter_thread.start()
    search_thread.start()

    for file_path in walk_sorted_files(root_directory):
        filter_queue.put(FilepathRegex(file_path, search_regex))

    # Signal completion to the queues.
    filter_queue.put(None)
    filter_thread.join()
    search_thread.join()


main()
