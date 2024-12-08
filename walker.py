#!/usr/bin/python

import os


class Walker:

    def __init__(self, full_path):
        self.path = full_path

    def walk_tree(self, folder_path = None):
        if folder_path is None:
            folder_path = self.path

        # traverse root directory, and list directories as dirs and files as files
        for root, dirs, files in os.walk(folder_path):
            print (list(os.scandir(root)))
            path = root.split(os.sep)
            print((len(path) - 1) * '---', os.path.basename(root))
            for file in files:
                print(len(path) * '---', file)

w = Walker("..")
w.walk_tree()