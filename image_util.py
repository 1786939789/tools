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

from file_util import read_detection_result_from_txt

def crawler_image_from_baidu(save_dir, keyword, page_count=1):
    """ crawl images from baidu
    
    Args:
        save_dir (str): images dir
        keyword (str): the keyword of images
        page_count (int): the count of pages
    """
    keyword_en = translate_chinese_to_english(keyword) if is_chinese(keyword) else keyword
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36",
        "referer": "https://image.baidu.com"
    }
    base_url = "https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1600411706254_R&pv=&ic=&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&sid=&word="
    keyword_utf8 = quote(keyword, encoding="utf-8")
    keyword_name = replace_underscore_with_space(keyword_en)
    check_dir(os.path.join(save_dir, keyword_name))
    num = 1
    for i in range(page_count):
        url = base_url + keyword_utf8 + "&pn=" + str(num)
        req = urllib.request.Request(url, headers=headers)
        f = urllib.request.urlopen(req).read().decode("utf-8")
        key = r'thumbURL":"(.+?)"'
        key1 = re.compile(key)
        for string in re.findall(key1, f):
            if "\\" in string:
                continue  
            print("Downloading {}".format(string))
            f_req = urllib.request.Request(string, headers=headers)
            f_url = urllib.request.urlopen(f_req).read()
            image_path = os.path.join(save_dir, keyword_name, keyword_name + str("_%06d"%(num)) + ".jpg")
            with open(image_path, "wb+") as fs:
                fs.write(f_url)
                fs.close()
            num += 1

def copy_image_by_xml(xml_dir, image_target_dir, image_dest_dir, image_suffix=".jpg"):
    """ copy the image through the xml of the same name
    
    Args:
        xml_dir (str): xml dir
        image_target_dir (str): image target dir
        image_dest_dir (str): image destination dir
        image_suffix (str): default .jpg
    """
    file_count = 0
    for file in os.listdir(xml_dir):
        filename = os.path.splitext(file)[0]
        suffix = os.path.splitext(file)[-1]
        if suffix not in [".xml"]:
            continue
        image_target_path = os.path.join(image_target_dir, filename + image_suffix)
        image_dest_path = os.path.join(image_dest_dir, filename + image_suffix)
        if os.path.isfile(image_target_path):
            shutil.copyfile(image_target_path, image_dest_path)
            file_count += 1
    print("Success: {} files have been copied.".format(file_count))

def download_image_by_url(url, save_dir):
    """ download images by url
    
    Args:
        url (str)
        save_dir (str)
    Return:
        True or False (bool)
    """
    check_dir(save_dir)
    filename = url.split("/")[-1]
    save_path = os.path.join(save_dir, filename)
    try:
        urllib.request.urlretrieve(url, filename=save_path)
        return True
    except Exception:
        return False

def is_3_channels(image_path):
    """ whether the image is 3 channels
    
    Args:
        image_path (str)
    """
    img = cv2.imread(image_path)
    try:
        h, w, c = img.shape
        if c == 3:
            return True
    except Exception:
        return False

def plot_one_box(img=None, x=None, label=None, color=None, line_thickness=None, fill=True):
    """ plot one bounding box on image 
    
    Args:
        img (numpy): original image
        x (list): the coordinate of bbox, such as [xmin, ymin, xmax, ymax]
        label (str): class and score will be put on the img
        color (tuple): the bgr value of color, for example, red is (0, 255, 0)
        line_thickness (int): the thickness of line thickness
        fill (bool): whether filled with color
    """
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        if (c1[1] - t_size[1] - 3) < 0: # set inside the box if it crosses the border
            c1 = c1[0], c1[1] + t_size[1]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        if fill:
            cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, (255, 255, 255), thickness=tf, lineType=cv2.LINE_AA)

def plot_dir_box(image_dir, save_dir, txt_file=None, detection_result=[]):
    """ plot bounding boxes on images in the image dir
    
    Args:
        image_dir (str): image dir
        save_dir (str): save dir
        txt_file (str): [optional] txt flie which storage detection result
        detection_result (list): [optional] enable use only when txt file is None
    """
    if txt_file is not None:
        result = read_detection_result_from_txt(txt_file)
    else:
        result = detection_result
    image_list = os.listdir(image_dir)
    image_list.sort()
    for i, image in enumerate(image_list):
        suffix = os.path.splitext(image)[-1]
        if suffix not in [".jpg", "jpeg", "png"]:
            continue
        img = cv2.imread(os.path.join(image_dir, image))
        for detection in result[i]:
            # text = detection[-2] + " " + detection[0] + "," + detection[1] + "," + detection[2] + "," + detection[3]
            plot_one_box(img, detection[:4], detection[-2], color=(128, 0, 128), line_thickness=1)
        cv2.imwrite(os.path.join(save_dir, image), img)

def png_to_jpg(png_path, jpg_path):
    """ convert image format: png -> jpg, then save picture with jpg
    
    Args:
        png_path (str)
        jpg_path (str)
    Return:
        True or False (bool)
    """
    img = Image.open(png_path)
    try:
        if len(img.split()) == 4:
            # prevent IOError: cannot write mode RGBA as BMP
            r, g, b, a = img.split()
            img = Image.merge("RGB", (r, g, b))
            img.convert('RGB').save(jpg_path, quality=100)
        else:
            img.convert('RGB').save(jpg_path, quality=100)
        return True
    except Exception:
        return False

def remove_xml_without_image(xml_dir, image_dir):
    """ remove xml files without corresponding images
    
    Args:
        xml_dir (str): xml files dir
        image_dir (str): images dir
    """
    file_count = 0
    for file in os.listdir(xml_dir):
        portion = os.path.splitext(file)
        if portion[-1] == ".xml":
            image_path = os.path.join(image_dir, portion[0] + ".jpg")
            if not os.path.isfile(image_path):
                file_count += 1
                os.remove(os.path.join(xml_dir, file))
    print("Success: {} xml files have been removed.".format(file_count))

def svg_to_jpg(svg_path, save_path, fmt=None):
    """ convert image format: svg -> jpg, then save picture with jpg
    
    Args:
        svg_path (str)
        save_path (str)
        fmt (str): such as "JPG", "PNG" and None (None is to pdf)
    Return:
        True or False (bool)
    """
    try:
        if fmt is not None:
            fmt.upper()
        drawing = svg2rlg(svg_path)
        renderPM.drawToFile(drawing, save_path, fmt=fmt)
        return True
    except Exception:
        return False


