import os
import cv2
import json
import random
import shutil
import numpy as np
try: 
    import xml.etree.cElementTree as ET 
except ImportError: 
    import xml.etree.ElementTree as ET

from tqdm import tqdm

def generate_xml(target_dir, image_name, image_width, image_height, detections):
    """ generate xml file
    
    Args:
        target_dir (str): target xml dir
        image_name (str): the name of image
        image_width (int): the width of image
        image_height (int): the height of image
        detections (list): e.g. [[xmin, ymin, xmax, ymax, label]...]
    """
    dom = make_xml(image_name, image_width, image_height, detections)
    xml_save_path = os.path.join(target_dir, image_name + '.xml')
    with open(xml_save_path, 'wb+') as f:
        f.write(dom.toprettyxml(indent='\t', encoding='utf-8'))

def get_w_h_from_xml(target_file):
    """ get width and height from xml file
    
    Args:
        target_file (str): xml file
    """
    tree = ET.ElementTree(file=target_file)  
    root = tree.getroot() 
    size = root.find("size")
    width = size.find("width").text
    height = size.find("height").text
    return width, height

def make_xml(image_name, image_width, image_height, detections):
    """ make a xml dom
    
    Args:
        image_name (str): the name of image
        image_width (int): the width of image
        image_height (int): the height of image
        detections (list): e.g. [[xmin, ymin, xmax, ymax, label]...]
    """
    node_root = Element('annotation')
    node_folder = SubElement(node_root, 'folder')
    node_folder.text = 'VOC'
    node_filename = SubElement(node_root, 'filename')
    node_filename.text = image_name + ".jpg"
    node_object_num = SubElement(node_root, 'object_num')
    node_object_num.text = str(len(detections))
    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text = str(image_width)
    node_height = SubElement(node_size, 'height')
    node_height.text = str(image_height)
    node_depth = SubElement(node_size, 'depth')
    node_depth.text = '3'
    for i in range(len(detections)):  
        node_object = SubElement(node_root, 'object')
        node_name = SubElement(node_object, 'name')
        node_name.text = detections[i][-1]
        node_pose = SubElement(node_object, 'pose')
        node_pose.text = 'Unspecified'
        node_truncated = SubElement(node_object, 'truncated')
        node_truncated.text = '1'
        node_difficult = SubElement(node_object, 'difficult')
        node_difficult.text = '0'

        node_bndbox = SubElement(node_object, 'bndbox')
        node_xmin = SubElement(node_bndbox, 'xmin')
        node_xmin.text = str(detections[i][0])
        node_ymin = SubElement(node_bndbox, 'ymin')
        node_ymin.text = str(detections[i][1])
        node_xmax = SubElement(node_bndbox, 'xmax')
        node_xmax.text = str(detections[i][2])
        node_ymax = SubElement(node_bndbox, 'ymax')
        node_ymax.text = str(detections[i][3])

    xml = tostring(node_root, pretty_print = True)
    dom = parseString(xml)
    return dom

def xml_to_json(xml_dir, json_file, predefined_categories=None):
    """ convert xml files to json file
        cruuently we do not support segmentation
    
    Args:
        xml_dir (str): xml dir
        json_file (str): json file
        predefined_categories (dict): default None
    """
    json_dict = {"image": [], "type": "instance", "annotations": [], "categories": []}
    categories = predefined_categories if predefined_categories is not None else {}
    bnd_id = 0
    xml_list = os.listdir(xml_dir)
    for file in xml_list:
        filename = os.path.splitext(file)[0]
        suffix = os.path.splitext(file)[-1]
        if suffix not in [".xml"]:
            continue
        tree = ET.parse(os.path.join(xml_dir, file))
        root = tree.getroot()
        image_file = filename + ".jpg"
        image_id = filename
        width, height = get_w_h_from_xml(os.path.join(xml_dir, file))
        image_info = {"file_name": filename, "height": height, "width": width, "id":image_id}
        json_dict["image"].append(image_info)
        for obj in root.findall("object"):
            category = obj.find("name").text
            if category not in categories.keys():
                categories[category] = len(categories) # defualt start from 0
            category_id = categories[category]
            bndbox = obj.find("bndbox")
            xmin = int(bndbox.find("xmin").text)
            ymin = int(bndbox.find("ymin").text)
            xmax = int(bndbox.find("xmax").text)
            ymax = int(bndbox.find("ymax").text)
            bnd_width, bnd_height = abs(xmax -xmin), abs(ymax - ymin)
            anntation_info = {
                'area': bnd_width*bnd_height, 'iscrowd': 0, 'image_id': image_id, 
                'bbox':[xmin, ymin, bnd_width, bnd_height],
                'category_id': category_id, 'id': bnd_id, 'ignore': 0,'segmentation': []
            }
            json_dict["annotations"].append(anntation_info)
            bnd_id += 1
    for (cate_id, cate) in enumerate(categories):
        cat = {'supercategory': 'none', 'id': cate_id, 'name': cate}
        json_dict["categories"].append(cat)
    with open(json_file, "w") as f:
        json.dump(json_dict, f)
    print("Success: {} xml files have been converted.".format(len(xml_list)))