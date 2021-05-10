#encoding=utf-8
import os
from tqdm import tqdm
from basicFun import XML as XML
from basicFun import FILES
try: 
    import xml.etree.cElementTree as ET 
except ImportError: 
    import xml.etree.ElementTree as ET

class XML_Tool():
    def __init__(self, xml_dir):
        super(XML_Tool, self).__init__()
        self.xml_dir = xml_dir

    def add_new_classes(self, refer_dir, classes=[]):
        """ Add some new classes from refer_dir's xml to self.xml_dir's xml

            :param refer_dir: folder used to store xml which add to xml_dir
            :param classes: some new calsses will been add to xml_dir's xml
        """
        if len(classes) == 0:
            print('[ERROR]: classes is empty!')
            return False
        xmls = [x for x in FILES.get_sorted_files(self.xml_dir) if ".xml" in x]
        for xml in xmls:
            xml_path = os.path.join(self.xml_dir, xml)
            refer_path = os.path.join(refer_dir, xml)
            if os.path.exists(refer_path):
                boxes = XML.read_objects(refer_path)
                tree = ET.ElementTree(file = xml_path)
                root = tree.getroot()
                for box in boxes:
                    if box['name'] in classes:
                        root = XML.add_tag(root, box)
                XML.write_xml(tree, xml_path) 
        print('[success]: add classes successfully')
        return True

    def replace_class(self, old_class=None, new_class=None):
        """ replace old_class with new_class in the self.xml_dir's xml

            :param old_class: will be replaced by new_class
            :param new_class: used to replace old_class
        """
        if not old_class or not new_class:
            print('[ERROR]: classes is empty!')
        xmls = [x for x in FILES.get_sorted_files(self.xml_dir) if ".xml" in x]
        count = 0 # the number of xmls will be replaced with new class
        pbar = tqdm(xmls)
        for xml in pbar:
            xml_path = os.path.join(self.xml_dir, xml)
            if os.path.exists(xml_path):
                tree = ET.ElementTree(file = xml_path)
                root = tree.getroot()
                for obj in root.findall('object'):
                    ob_name = obj.find("name")
                    if ob_name.text in old_class:
                        ob_name.text = new_class
                        count += 1
                XML.write_xml(tree, xml_path)
            pbar.set_description("Processing %s" % xml)
        print('[success]: replace class successfully. %d instances have been modified here'%count)
        return True
    
    def replace_all_classes(self, new_class=None):
        """ replace all class with new_class in the self.xml_dir's xml

            :param new_class: used to replace all class
        """    
        if not new_class:
            print('[ERROR]: classes is empty!')
        xmls = [x for x in FILES.get_sorted_files(self.xml_dir) if ".xml" in x]
        for xml in xmls:
            xml_path = os.path.join(self.xml_dir, xml)
            if os.path.exists(xml_path):
                tree = ET.ElementTree(file = xml_path)
                root = tree.getroot()
                for obj in root.findall('object'):
                    ob_name = obj.find("name")
                    ob_name.text = new_class
                XML.write_xml(tree, xml_path)
        print('[success]: replace class successfully')
        return True
    
    def count_classes(self):
        """ count how many classes there are

        """
        xmls = [x for x in FILES.get_sorted_files(self.xml_dir) if ".xml" in x]
        classes = {}
        for xml in xmls:
            xml_path = os.path.join(self.xml_dir, xml)
            if os.path.exists(xml_path):
                tree = ET.ElementTree(file = xml_path)
                root = tree.getroot()
                classes_ = []
                for obj in root.findall('object'):
                    name = obj.find('name').text
                    # if name not in classes_:
                    #     classes_.append(name)
                    # else:
                    #     continue
                    if name not in classes:
                        classes[name] = 1
                    else:
                        classes[name] += 1
        return classes
    
    def xml_to_json(self, txt_path=None, json_path=None):
        pass
        
    def get_xml_by_class(self, classes=[], txt_path=None):
        """ get specified xmls to txt by classes

            :param classes: specified classes
            :txt_path: save xml list to txt
        """
        if len(classes) == 0:
            print('[ERROR]: classes is empty!')
            return False
        xmls = [x for x in FILES.get_sorted_files(self.xml_dir) if ".xml" in x]
        for xml in xmls:
            xml_path = os.path.join(self.xml_dir, xml)
            if os.path.exists(xml_path):
                tree = ET.ElementTree(file = xml_path)
                root = tree.getroot()
                for obj in root.findall('object'):
                    name = obj.find('name').text
                    if name in classes:
                        portion = os.path.splitext(xml)
                        with open(txt_path, 'a') as f:
                            f.write( portion[0] + '\n')
                        break
        print('[success]: save successfully')
        return True

    def get_xml_by_classes_from_txt(self, txt_src=None, classes=[], txt_path=None):
        """ get specified xmls to txt by classes

            :param classes: specified classes
            :txt_path: save xml list to txt
        """
        if len(classes) == 0:
            print('[ERROR]: classes is empty!')
            return False
        list_fp = open(txt_src, 'r')
        for line in list_fp:
            xml = line.strip() + '.xml' # xml line
            xml_path = os.path.join(self.xml_dir, xml)
            if os.path.exists(xml_path):
                tree = ET.ElementTree(file = xml_path)
                root = tree.getroot()
                for obj in root.findall('object'):
                    name = obj.find('name').text
                    if name in classes:
                        portion = os.path.splitext(xml)
                        with open(txt_path, 'a') as f:
                            f.write( portion[0] + '\n')
                        break
        print('[success]: save successfully')
        return True

    def delete_class(self, classes=[]):
        pass
if __name__=="__main__":
    xml_dir = "E:/Primitive_Arguments/flag_person/xml/"
    refer_dir = "E:/Primitive_Arguments/flag/detection/flag/xml_flag/"
    # old_class = 'riders'
    # new_class = 'person' 
    xml = XML_Tool(xml_dir)
    # xml.replace_class(old_class, new_class)
    # xml.add_new_classes(refer_dir, ["flag"])
    print(xml.count_classes())

