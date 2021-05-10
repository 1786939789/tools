import os
try: 
    import xml.etree.cElementTree as ET 
except ImportError: 
    import xml.etree.ElementTree as ET  
from bs4 import BeautifulSoup
def draw_xml(objs_s,tarXml):
    if len(objs_s)>0:
        tree = ET.ElementTree(file=tarXml)
        root = tree.getroot()
        for obj in objs_s:
            add_tag(root,obj)
            write_xml(tree,tarXml)
def add_tag(root,BBox={"name","xmin","ymin","xmax","ymax"},tag="object",insertPlace=6):
    index=insertPlace
    object=ET.Element(tag)
    name=ET.SubElement(object,"name")
    pose = ET.SubElement(object, "pose")
    truncated = ET.SubElement(object, "truncated")
    difficult = ET.SubElement(object, "difficult")
    bndbox = ET.SubElement(object, "bndbox")
    name.text = BBox["name"]
    xmin = ET.SubElement(bndbox, "xmin")
    ymin = ET.SubElement(bndbox, "ymin")
    xmax = ET.SubElement(bndbox, "xmax")
    ymax = ET.SubElement(bndbox, "ymax")
    xmin.text=BBox["xmin"]
    ymin.text=BBox["ymin"]
    xmax.text=BBox["xmax"]
    ymax.text=BBox["ymax"]
    pose.text="Unspecified"
    truncated.text="0"
    difficult.text="0"
    # ET.dump(object)
    root.insert(index,object)
    return root
def chag_filename(root,filename,tag="filename"):
    for obj in root.findall(tag):
        if obj.text!= filename:
            print(filename)
            obj.text= filename
def chag_label(root,labelDict,tag="object"):
    for obj in root.findall(tag):
        ob_name=obj.find("name")
        if ob_name.text in labelDict.keys():
            ob_name.text=labelDict[ob_name.text]
    return root
def chag_size(root,width=0,height=0,tag="size"):
    for siz in root.findall(tag):
        siz_width=siz.find("width")
        siz_height=siz.find("height")
        if siz_width.text!=str(width) or siz_height.text!=str(height):
            print('Change size ({},{}) to ({},{})'.format(siz_width.text,siz_height.text,width,height))
            siz_width.text=str(width)
            siz_height.text=str(height)
def del_all_tag(root,tag="object"):
    for obj in root.findall(tag):
        ob_name=obj.find("name")
        root.remove(obj)
    return root
def del_tag(root, nameList, tag="object"):
    for obj in root.findall(tag):
        ob_name=obj.find("name")
        if ob_name.text in nameList:
            root.remove(obj)
    return root
def read_objects(path=None):
    if path==None:
        print("[ERROR ] Path is None!")
        return []
    objs=[]
    with open(path,'rb') as fr:
        all_txt=fr.read()
        soup=BeautifulSoup(all_txt,"lxml")
        m_objects=soup.find_all('object')
        for m_object in m_objects:
            name=m_object.find_all("name")[0].get_text()
            xmin=m_object.find_all("xmin")[0].get_text()
            ymin=m_object.find_all("ymin")[0].get_text()
            xmax=m_object.find_all("xmax")[0].get_text()
            ymax=m_object.find_all("ymax")[0].get_text()
            objs.append({"name":name,
                "xmin":xmin,"ymin":ymin,"xmax":xmax,"ymax":ymax})
    return objs
def read_objects_exclude_minsize(path=None):
    if path==None:
        print("[ERROR ] Path is None!")
        return []
    objs=[]
    with open(path,'rb') as fr:
        all_txt=fr.read()
        soup=BeautifulSoup(all_txt,"lxml")
        m_objects=soup.find_all('object')
        for m_object in m_objects:
            name=m_object.find_all("name")[0].get_text()
            xmin=m_object.find_all("xmin")[0].get_text()
            ymin=m_object.find_all("ymin")[0].get_text()
            xmax=m_object.find_all("xmax")[0].get_text()
            ymax=m_object.find_all("ymax")[0].get_text()
            width=abs(int(xmin)-int(xmax))
            height=abs(int(ymin)-int(ymax))
            if name in ['blue','yellow','red','gray','security','other']:
                if height<100 and width<50:
                    continue
            objs.append({"name":name,
                "xmin":xmin,"ymin":ymin,"xmax":xmax,"ymax":ymax})
    return objs
def read_boxes(path=None):
    if path==None:
        print("[ERROR ] Path is None!")
        return []
    boxes=[]
    with open(path,'rb') as fr:
        all_txt=fr.read()
        soup=BeautifulSoup(all_txt,"lxml")
        m_objects=soup.find_all('object')
        for m_object in m_objects:
            xmin=m_object.find_all("xmin")[0].get_text()
            ymin=m_object.find_all("ymin")[0].get_text()
            xmax=m_object.find_all("xmax")[0].get_text()
            ymax=m_object.find_all("ymax")[0].get_text()
            boxes.append([float(int(xmin)),float(int(ymin)),float(int(xmax)),float(int(ymax)),1.0])
    return boxes
def right_filename(root,filename,tag="filename"):
    for obj in root.findall(tag):
        if obj.text!= filename:
            return False
    return True
def right_size(root,width=0,height=0,tag="size"):
    for siz in root.findall(tag):
        siz_width=siz.find("width")
        siz_height=siz.find("height")
        if siz_width.text!=str(width) or siz_height.text!=str(height):
            # print('Unmatch size ({},{}) with ({},{})'.format(siz_width.text,siz_height.text,width,height))
            return False
    return True
def save_tag(root, svNames, tag="object"):
    for obj in root.findall(tag):
        ob_name=obj.find("name")
        if ob_name.text not in svNames:
            root.remove(obj)
    return root
def thresh_size(root,width,sizeThreshDict,tag="object"):
    for obj in root.findall(tag):
        ob_name=obj.find("name")
        if ob_name.text in sizeThreshDict.keys():
            xsize=int(obj.find("bndbox").find('xmax').text)-int(obj.find("bndbox").find('xmin').text)
            ysize=int(obj.find("bndbox").find('ymax').text)-int(obj.find("bndbox").find('ymin').text)
            if xsize<sizeThreshDict[ob_name.text][0]*width/1920 or ysize<sizeThreshDict[ob_name.text][1]*width/1920:
                root.remove(obj)
    return root   
def write_xml(tree, out_path):
    tree.write(out_path, encoding="utf-8",xml_declaration=True)
    # print("write")
def info():
    print('add_tag(root,BBox=["name","xmin","xmax","ymin","ymax"],tag="object",insertPlace=6) -> ET.root')
    print('del_tag(root, nameList, tag="object") -> ET.root')
    print("read_object(path=None) -> list=[name,xmin,xmax,ymin,ymax]")
    print("write_xml(tree, out_path) -> void")
    exit()
