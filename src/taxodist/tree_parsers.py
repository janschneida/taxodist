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