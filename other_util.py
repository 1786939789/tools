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

def is_number(target_str):
    """ determine whether the word is number
    
    Args:
        target_str (str): target string
    """
    try:
        float(target_str)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(target_str)
        return True
    except (TypeError, ValueError):
        pass
    return False

def is_chinese(target_str):
    """ determine whether the word is Chinese
    
    Args:
        target_str (str): target string
    """
    for ch in target_str:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

def replace_underscore_with_space(target_str):
    """ replace spaces with underscores
    
    Args:
        target_str (str): target string
    """
    return "_".join(target_str.split(" "))

def translate_chinese_to_english(target_str):
    """ translate Chinese to English
    
    Args:
        target_str (str): target string
    """
    translator = Translator(from_lang="chinese",to_lang="english")
    result = translator.translate(target_str)
    return result.lower()

def translate_english_to_chinese(target_str):
    """ translate English to Chinese
    
    Args:
        target_str (str): target string
    """
    translator = Translator(to_lang="chinese")
    result = translator.translate(target_str)
    return result
