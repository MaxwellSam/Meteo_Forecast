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
    print("\npath_old ", path_old_dir)
    print("\npath_new ", path_new_dir)

    # creat dir if not exist
    if not os.path.exists(os.path.normpath(path_old_dir)):
        os.makedirs(os.path.normpath(path_old_dir))
    if not os.path.exists(os.path.normpath(path_old_dir)):
        os.makedirs(os.path.normpath(path_new_dir))
    # move files to archive
    all_files = os.listdir(os.path.normpath(path_old_dir))
    for f in all_files:
        old_file_path = os.path.normpath(path_old_dir+f)
        new_file_path = os.path.normpath(path_new_dir+f)
        # if os.path.exists(new_file_path):
        #     os.remove(new_file_path)
        if os.path.isfile(new_file_path):
            os.remove(new_file_path)
        print("\nfiles => ", all_files)
        print("\nnew => ", new_file_path)
        print("\nold => ", old_file_path)
        os.rename(old_file_path, new_file_path) 