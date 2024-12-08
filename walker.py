#!/usr/bin/python

import os


class Walker:

    def __init__(self, full_path):
        self.path = full_path

    def walk_tree(self, folder_path = None):
        if folder_path is None:
            folder_path = self.path

        # traverse root directory, and list directories as dirs and files as files
        subdirs_to_check = []
        for direntry in os.scandir(folder_path):
            if direntry.is_dir():
                subdirs_to_check.append(direntry)
            else:
                path = direntry.path.split(os.sep)
                print((len(path) - 1) * '---', os.path.basename(direntry.path), direntry.stat())

        for direntry in subdirs_to_check:
            print()
            print (direntry.path)
            self.walk_tree(folder_path = direntry.path)

w = Walker("..")
w.walk_tree()