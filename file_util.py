import os
import re
import cv2
import json
import pandas
import random
import shutil
import urllib.request
import numpy as np
try: 
    import xml.etree.cElementTree as ET 
except ImportError: 
    import xml.etree.ElementTree as ET

from tqdm import tqdm
from urllib.parse import quote
from translate import Translator

def check_dir(target_dir):
    """ if target dir is not exist, then create a new dir  

    Args:
        target_dir (str): e.g. /xx/xx/
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print("Success: {} has been created".format(target_dir))
    else:
        print("Success: {} has existed".format(target_dir))

def copy_files(target_dir, dest_dir, filter_str=None):
    """ copy files according to the filter string
    
    Args:
        target_dir (str): target dir
        dest_dir (str): destination dir
        filter_str (str): filter string
    """
    file_count = 0
    for file in os.listdir(target_dir):
        name = os.path.splitext(file)[0]
        if filter_str is None:
            file_count += 1
            shutil.copyfile(os.path.join(target_dir, file), os.path.join(dest_dir, file))
        elif filter_str in file:
            file_count += 1
            shutil.copyfile(os.path.join(target_dir, file), os.path.join(dest_dir, file))
    print("Success: {} files have been copied.".format(file_count))

def files_rename(target_dir, prefix=None):
    """ batch file rename within the target dir
    
    Args:
        target_dir (str): e.g. /xx/xx/
        prefix (str): file prefix
    """
    image_id = 0
    if prefix is not None:
        prefix += "_"
    else:
        prefix = ""
    for file in os.listdir(target_dir):
        image_id += 1
        suffix = os.path.splitext(file)[-1]
        new_file = prefix + str("%06d"%image_id) + suffix
        os.rename(os.path.join(target_dir, file), os.path.join(target_dir, new_file))
    print("Success: {} files have been processed.".format(image_id))

def multiple_folders_to_one(src_dir, dest_dir):
    """ combine files from multiple folders into one folder
        note that all files cannot have the same name, otherwise they will be overwritten
    
    Args:
        src_dir (str): there are multiple folders within the src_dir
        dest_dir (str): destination dir
    """
    file_count = 0
    for root, dirs, files in os.walk(src_dir):
        files.sort()
        for file in files:
            shutil.copyfile(os.path.join(root, file), os.path.join(dest_dir, file))
            file_count += 1
    print("Success: {} files have been processed.".format(file_count))

def read_detection_result_from_txt(target_file):
    """ read detection result from txt
        storage format in the txt: xmin, ymin, xmax, ymax, label, score; ...
    
    Args:
        target_file (str): txt file
    """
    result = []
    with open(target_file, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            detection = []
            for le in line.split(";"):
                if le[0] == "\n":
                    continue
                detection.append(le.split(",")) # correspond to one box
            result.append(detection)
    return result

def read_excel(excel_path, coloum_name=None):
    """ read excel file and return the specified column
    
    Args:
        csv_path (str)
        coloum_name (str)
    Return:
        description_list (list)
    """
    suffix = os.path.splitext(excel_path)[-1]
    if suffix == ".csv":
        excel_data = pandas.read_csv(excel_path)
    elif suffix == ".xlsx":
        excel_data = pandas.read_excel(excel_path)
    if coloum_name is None:
        return excel_data
    else:
        return excel_data[coloum_name].tolist()
