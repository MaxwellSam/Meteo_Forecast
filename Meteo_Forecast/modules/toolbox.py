"""
File: toolbox.py
Path: 
Description: Usefull methods for Meteo Forecast program
Author: Sam Maxwell
Date: 03/2022
"""
## import ##
import os


def move_dir_content(path_old_dir, path_new_dir):
    all_files = os.listdir(path_old_dir)
    for f in all_files:
        os.rename(path_old_dir+f, path_new_dir+f) 