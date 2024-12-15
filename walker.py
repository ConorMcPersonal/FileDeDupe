#!/usr/bin/python

import os
import socket
import argparse
import datetime

import pandas as pd

class Walker:

    def __init__(self, full_path, config = 'Base'):
        self.path = os.path.abspath(full_path)
        self.host = socket.gethostname()
        self.codeversion = '0.1'
        self.config = config
        self.results = []
        self.dircount = 0
    
    def is_image(self, filename: str):
        endings = {'.jpg', '.jpeg', '.jpe', '.gif', '.png'}
        suff = self.get_suffix(filename)
        return (suff, suff in endings)

    def get_suffix(self, filename):
        filename = filename.lower()
        f, suff = os.path.splitext(filename)
        return suff

    def walk_tree(self, folder_path = None):
        if folder_path is None:
            folder_path = self.path

        abspath = os.path.abspath(folder_path)
        #print()
        #print(abspath, 'on', self.host)
        # traverse root directory, and list directories as dirs and files as files
        subdirs_to_check = []
        try:
            direntries = os.scandir(folder_path)
        except PermissionError:
            #Access denied
            return
        
        self.dircount += 1
        if self.dircount % 300 == 0:
            print()
            print(abspath, 'on', self.host, f'({self.dircount} / {len(self.results)})')
        else:
            print (".", end  = '')


        for direntry in direntries:
            if direntry.is_dir():
                subdirs_to_check.append(direntry)
            else:
                try:
                    fsize = direntry.stat().st_size
                except FileNotFoundError:
                    fsize = -1
                path = direntry.path.split(os.sep)
                fname = os.path.basename(direntry.path)
                suff = self.get_suffix(fname)
                self.results.append({'folder': abspath, 'fname': fname, 'suffix': suff, 'size': fsize})
                #print((len(path) - 1) * '---', fname, direntry.stat(), suff)

        for direntry in subdirs_to_check:
            self.walk_tree(folder_path = direntry.path)

    def get_results_df(self):
        df = pd.DataFrame(self.results)
        df['host'] = self.host
        df['config'] = self.config
        df['codeversion'] = self.codeversion
        return df
    
def create_parser():
    parser = argparse.ArgumentParser(description="File Catalogue Builder")
    parser.add_argument("-p", "--path", help="Path to scan", required = True, metavar = "<path to scan>")
    parser.add_argument("-c", "--config", help="Config name (default: Base) - useful if scanning USB drives", metavar = "<config name>")
    parser.add_argument("-o", "--output", help="Folder in which to save the output as a parquet file. Default is current directory.", metavar = "<output directory>")
    return parser

def main():
    parser = create_parser()
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        return

    path_to_scan = os.path.abspath(args.path)
    config_name = 'Base'
    if args.config:
        config_name = args.config
    output_path  = "."
    if args.output:
        output_path = args.output
    output_path = os.path.abspath(output_path)

    print (f"Scanning: {path_to_scan} with Config Name: {config_name}. Output to :{output_path}")

    w = Walker(path_to_scan, config = config_name)
    try:
        w.walk_tree()
    except:
        print ("Error encountered, will still writre partial result set.")
    df = w.get_results_df()
    fname = os.path.join(output_path, datetime.datetime.isoformat(datetime.datetime.now()).replace(":", "") + '.pq')
    df.to_parquet(fname)
    print ("Saved as ", fname)

if __name__ == "__main__":
    main()
