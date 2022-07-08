from re import A
import treelib
import xml.etree.ElementTree as ET
from src.taxodist import td_utils as utils

def getICD10GMTree(version = '2022'):
    """
    Returns a tree that represents the ICD-10-GM taxonomy. \n
    Based on the ICD-10-XML export from https://www.dimdi.de/dynamic/de/klassifikationen/downloads/
    """
    if(version == '2021'):
        raw_xml = ET.parse('resources\\ICD_10_GM_2021.xml')
    elif(version == '2022'):
        raw_xml = ET.parse('resources\\ICD_10_GM_2022.xml')
    root = raw_xml.getroot()
    tree = treelib.Tree()
    tree.create_node('ICD-10', 0)

    # create all nodes
    for clss in root.iter('Class'):
        tree.create_node(clss.get('code'), clss.get('code'), parent=0)

    # move them to represent the hierarchy
    for clss in root.iter('Class'):
        if clss.get('kind') != 'chapter':
            for superclass in clss.iter('SuperClass'):
                tree.move_node(clss.get('code'), superclass.get('code'))
    
    # add modifier codes
    for clss in root.iter('Class'):
        parent_name = clss.get('code')
        parent = tree.get_node(parent_name)
        
        class_mods = clss.findall('ModifiedBy')
        if len(class_mods) > 1:
            for mod1 in root.iter('Modifier'):
                if mod1.get('code') == class_mods[0].get('code'):
                    for val1 in mod1.iter('SubClass'):
                        for mod2 in root.iter('Modifier'):
                            if mod2.get('code') == class_mods[1].get('code'):
                                for val2 in mod2.iter('SubClass'):
                                    node_name = parent_name+val1.get('code')+val2.get('code')
                                    tree.create_node(node_name, node_name, parent=parent)
        else:
            for cls_mod in clss.iter('ModifiedBy'):
                if cls_mod.get('all') == 'false':
                    for modclass in clss.iter('ValidModifierClass'):
                        node_name = parent_name+modclass.get('code')
                        tree.create_node(node_name, node_name, parent=parent)
                else:
                    #find corresponding modifier
                    for mod in root.iter('Modifier'):
                        # get values of class modifier
                        if mod.get('code') == cls_mod.get('code'):
                            for value in mod.iter('SubClass'):
                                node_name = parent_name+value.get('code')
                                tree.create_node(node_name, node_name, parent=parent)
    
    return tree

def getICDO3Tree():
    """
    Returns a tree that represents the ICD-O-3 taxonomy. \n
    Based on the ICD-O-3-XML export from https://www.bfarm.de/DE/Kodiersysteme/Services/Downloads/_node.html
    """
    raw_xml = ET.parse('resources\\ICD_O_3_2019.xml')
    root = raw_xml.getroot()
    tree = treelib.Tree()
    tree.create_node('ICD-O-3', 0)

    # create all nodes
    for clss in root.iter('Class'):
        tree.create_node(clss.get('code'), clss.get('code'), parent=0)

    # move them to represent the hierarchy
    for clss in root.iter('Class'):
        if clss.get('kind') != 'chapter':
            for superclass in clss.iter('SuperClass'):
                tree.move_node(clss.get('code'), superclass.get('code'))

    return tree

def getICD10WHOTree():
    """
    Returns a tree that represents the ICD-10-WHO taxonomy. \n
    Based on the ICD-10-WHO-XML export from https://www.bfarm.de/DE/Kodiersysteme/Services/Downloads/_node.html
    """
    raw_xml = ET.parse('resources\\ICD_10_WHO_2019.xml')
    root = raw_xml.getroot()
    tree = treelib.Tree()
    tree.create_node('ICD-10-WHO', 0)

    # create all nodes
    for clss in root.iter('Class'):
        tree.create_node(clss.get('code'), clss.get('code'), parent=0)

    # move them to represent the hierarchy
    for clss in root.iter('Class'):
        if clss.get('kind') != 'chapter':
            for superclass in clss.iter('SuperClass'):
                tree.move_node(clss.get('code'), superclass.get('code'))

    return tree

def getICD10CMTree():
    """
    Returns a tree that represents the ICD-10-CM taxonomy. \n
    Based on the ICD-10-CM-XML export from
    """
    raw_xml = ET.parse('resources\\ICD_10_CM_2022.xml')
    root = raw_xml.getroot()
    tree = treelib.Tree()
    tree.create_node('ICD-10-CM', 0)

    # iterate over chapters, sections & diags to create tree
    for chapter in root.iter('chapter'):
        chapter_node = tree.create_node(chapter.find('name').text, chapter.find('name').text, parent=0)
        for section in chapter.iter('section'):
            section_node = tree.create_node(section.get('id'), section.get('id'), parent=chapter_node)
            utils.iterateOverDiags(section,section_node,tree)

    return tree