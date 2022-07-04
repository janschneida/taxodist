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
    
    # manually add F10 codes https://www.dimdi.de/static/de/klassifikationen/icd/icd-10-gm/kode-suche/htmlgm2022/block-f10-f19.htm
    parent = tree.get_node('F10')
    for i in range(0,10):
        node_name = 'F10.' + str(i)
        tree.create_node(node_name,node_name,parent=parent)
        
    # manually add K25-K28 codes https://www.dimdi.de/static/de/klassifikationen/icd/icd-10-gm/kode-suche/htmlgm2022/block-k20-k31.htm
    parent = tree.get_node('K20-K31')
    for i in range(25,29):
        for j in range(0,10):
            node_name = 'K'+str(i)+'.'+str(j)
            tree.create_node(node_name,node_name,parent=parent)
            
    # manually add J96 codes https://www.dimdi.de/static/de/klassifikationen/icd/icd-10-gm/kode-suche/htmlgm2022/block-j95-j99.htm#J96
    addJ96Codes(tree)
    
    # manually add N17-N19 codes https://www.dimdi.de/static/de/klassifikationen/icd/icd-10-gm/kode-suche/htmlgm2022/block-n17-n19.htm#N17
    addN17_N19Codes(tree)
    
    # manually add M40-M54 codes https://www.dimdi.de/static/de/klassifikationen/icd/icd-10-gm/kode-suche/htmlgm2022/block-m50-m54.htm#M54
    addM40_M54Codes(tree)
    
    # manually add M70-M79 codes https://www.dimdi.de/static/de/klassifikationen/icd/icd-10-gm/kode-suche/htmlgm2022/block-m70-m79.htm#M79
    addM70_M79Codes(tree)
    
    # manually add E10-E14 codes https://www.dimdi.de/static/de/klassifikationen/icd/icd-10-gm/kode-suche/htmlgm2022/block-e10-e14.htm#E11
    addE10_E14Codes(tree)
    
    # manually add M91-M94 codes https://www.dimdi.de/static/de/klassifikationen/icd/icd-10-gm/kode-suche/htmlgm2022/block-m91-m94.htm#M93
    addM91_M94Codes(tree)
    
    # manually add K80-K87 codes https://www.dimdi.de/static/de/klassifikationen/icd/icd-10-gm/kode-suche/htmlgm2022/block-k80-k87.htm#K80
    addK80_K87Codes(tree)
    
    # manually addJ44 codes
    addJ44Codes(tree)
    addI10_I15Codes(tree)

    return tree

def addJ96Codes(tree: treelib.Tree):
    node_names = ['J96.00','J96.01','J96.09',
                  'J96.10','J96.11','J96.19',
                  'J96.90','J96.91','J96.99']
    for node_name in node_names:
        parent_id = node_name[:len(node_name)-1]
        parent = tree.get_node(parent_id)
        tree.create_node(node_name,node_name,parent=parent)
    return

def addM40_M54Codes(tree: treelib.Tree):
    
    # M40
    for i in range(0,6):
        for j in range(0,10):
            node_name = 'M40.'+str(i)+str(j)
            parent_id = node_name[:len(node_name)-1]
            parent = tree.get_node(parent_id)
            tree.create_node(node_name,node_name,parent=parent)
    
    # M41
    for i in [0,1,2,3,4,5,8,9]:
        for j in range(0,10):
            node_name = 'M41.'+str(i)+str(j)
            parent_id = node_name[:len(node_name)-1]
            parent = tree.get_node(parent_id)
            tree.create_node(node_name,node_name,parent=parent)
    
    # M42    
    for parent_id in ['M42.0','M42.1','M42.9']:
        parent = tree.get_node(parent_id)
        for i in range(0,10):
            node_name = parent_id + str(i)
            tree.create_node(node_name,node_name,parent=parent)
    
    # M43
    for parent_id in ['M43.0','M43.1','M43.2','M43.5','M43.8','M43.9']:
        parent = tree.get_node(parent_id)
        for i in range(0,10):
            # M43.5 - Sonstige habituelle Wirbelsubluxation [5. Stelle: 0,2-9]
            if i == 1 and node_name == 'M43.5':
                continue
            node_name = parent_id + str(i)
            tree.create_node(node_name,node_name,parent=parent) 
    
    # M53 & M54      
    for parent_id in ['M53.2','M53.8','M53.9','M54.0','M54.1','M54.8','M54.9']:
        parent = tree.get_node(parent_id)
        for i in range(0,10):
            node_name = parent_id+str(i)
            tree.create_node(node_name,node_name,parent=parent)
    
    return

def addN17_N19Codes(tree: treelib.Tree):
    stadien = ['1','2','3','9']  
    for parent_id in ['N17.0','N17.1','N17.2','N17.8','N17.9']:
        for i in stadien:
            node_name = parent_id+i
            parent = tree.get_node(parent_id)
            tree.create_node(node_name,node_name,parent=parent) 
    return

def addM70_M79Codes(tree: treelib.Tree):
    # M71
    for parent_id in ['M71.0','M71.1','M71.3','M71.4','M71.5','M71.8','M71.9']:
        parent = tree.get_node(parent_id)
        for i in range(0,10):
            node_name = parent_id+str(i)
            tree.create_node(node_name,node_name,parent=parent)  
    
    # M72
    for parent_id in ['M72.4','M72.6','M72.8','M72.9']:
        parent = tree.get_node(parent_id)
        for i in range(0,10):
            node_name = parent_id+str(i)
            tree.create_node(node_name,node_name,parent=parent) 
    
    # M73
    for parent_id in ['M73.0','M73.1','M73.8']:
        parent = tree.get_node(parent_id)
        for i in range(0,10):
            node_name = parent_id+str(i)
            tree.create_node(node_name,node_name,parent=parent) 
    
    # M72
    for parent_id in ['M79.0','M79.1','M79.3','M79.5','M79.6','M79.8','M79.9']:
        parent = tree.get_node(parent_id)
        for i in range(0,10):
            if i == 8 and node_name == 'M79.6':
                continue
            node_name = parent_id+str(i)
            tree.create_node(node_name,node_name,parent=parent)
    tree.create_node('M79.46','M79.46',parent=tree.get_node('M79.4'))         
    tree.create_node('M79.70','M79.70',parent=tree.get_node('M79.7'))
    
    return

def addE10_E14Codes(tree: treelib.Tree):
    for parent_id in ['E10','E11','E12','E13','E14']:
        parent = tree.get_node(parent_id)
        for i in range(0,10):
            for j in range (0,6):
                node_name = parent_id+'.'+str(i)+str(j)
                tree.create_node(node_name,node_name,parent=parent)  
    return

def addM91_M94Codes(tree: treelib.Tree):
    for parent_id in ['M93.2','M93.8','M94.2','M94.3','M94.8','M94.9']:
        parent = tree.get_node(parent_id)
        for i in range(0,10):
            node_name = parent_id+str(i)
            tree.create_node(node_name,node_name,parent=parent)  
    return

def addK80_K87Codes(tree: treelib.Tree):
    for parent_id in ['K80.0','K80.1','K80.2','K80.3','K80.4','K80.5','K80.8']:
        parent = tree.get_node(parent_id)
        for i in range(0,2):
            node_name = parent_id+str(i)
            tree.create_node(node_name,node_name,parent=parent)
            
    for parent_id in ['K85.0','K85.1','K85.2','K85.3','K85.8','K85.9']:
        parent = tree.get_node(parent_id)
        for i in range(0,2):
            node_name = parent_id+str(i)
            tree.create_node(node_name,node_name,parent=parent)  
    return


def addJ44Codes(tree: treelib.Tree):
    for parent_id in ['J44.0','J44.1','J44.8','J44.9']:
        parent = tree.get_node(parent_id)
        for i in [0,1,2,3,9]:
            node_name = parent_id+str(i)
            tree.create_node(node_name,node_name,parent=parent)
    return

def addI10_I15Codes(tree: treelib.Tree):
    subtree = tree.subtree('I10-I15')
    nodes =  subtree.all_nodes()
    for node in nodes:
        if node.is_leaf():
            parent_id = node.tag
            parent = tree.get_node(parent_id)
            for i in range(0,2):
                node_name = parent_id+str(i)
                tree.create_node(node_name,node_name,parent=parent)
    return

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