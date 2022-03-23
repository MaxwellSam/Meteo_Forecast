"""
File: toolbox.py
Path: 
Description: Usefull methods for Meteo Forecast program
Author: Sam Maxwell
Date: 03/2022
"""
## import ##
import os
import requests

# ----------------- methods ----------------------

# ---------------- fetch data --------------------

def fetch_url(url):
    try:
        return requests.get(url, verify=False)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


# -------------- files management -----------------

def move_dir_content(path_old_dir, path_new_dir):
    # creat dir if not exist
    if not os.path.exists(os.path.normpath(path_old_dir)):
        print("# Creat directory '{}' ... ".format(os.path.normpath(path_old_dir)), end="")
        os.makedirs(os.path.normpath(path_old_dir))
        print("Done")
    if not os.path.exists(os.path.normpath(path_old_dir)):
        print("# Creat directory '{}' ... ".format(os.path.normpath(path_new_dir)), end="")
        os.makedirs(os.path.normpath(path_new_dir))
        print("Done")
    # move files to archive
    all_files = os.listdir(os.path.normpath(path_old_dir))
    for f in all_files:
        old_file_path = os.path.normpath(path_old_dir+f)
        new_file_path = os.path.normpath(path_new_dir+f)
        if os.path.isfile(new_file_path):
            print("# File '{}' allready exit in archive, remove file ... ".format(f), end="")
            os.remove(new_file_path)
            print("Done")
        print("# Move file '{}' to archive ... ".format(f), end="")
        os.rename(old_file_path, new_file_path)
        print("Done") 