import io
import json
import os
import re
import xml.etree.ElementTree as ETx
from collections import ChainMap
from collections import defaultdict
from pprint import pprint
from itertools import groupby


'''Reading in a sample XML'''
# Need to read the xml file but also need to manipulate it since it will be incorrectly structured by default.
# this requires converting it into a string and then manipulating it.
# Manipulating the initial XML will be incredibly tedious due to the format it comes in from DrawIO.
# Use encoding="unicode" to generate a Unicode string (otherwise, a bytestring is generated).
# https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.tostring
# https://stackoverflow.com/questions/18575063/how-to-create-a-list-of-elements-from-an-xml-file-in-python
# https://docs.python.org/3/library/re.html
# https://stackoverflow.com/questions/19367373/regex-for-remove-everything-after-with


tree = ETx.parse("simple_password_reset.drawio")
root = tree.getroot()
xmlstr = ETx.tostring(root, encoding='unicode',
                      method='xml')  # unicode not utf-8
strx = """math="0" shadow="0">"""
pattern = "^[^³]*" + strx + "\n"         # will match all text until it finds the string (plus newline removal)
xmlstr = re.sub(pattern, '', xmlstr)

stry = "        </mxGraphModel>"
pattern = stry + "[^|]*$"
xmlstr = re.sub(pattern, '', xmlstr)

xmlfinal = ETx.ElementTree(ETx.fromstring(xmlstr))
rootfinal = xmlfinal.getroot()
tags = {elem.tag for elem in rootfinal.iter()}

# pattern = "^(.*)(?=<root)" # this is correct, but it doesn't work…presumably because of the way the parsing is done.
# xmlstr = re.sub("^(.*)(?=<root)", '', xmlstr)
# print(xmlstr)
# print(rootfinal.tag)  # checking that root is our overall parent
# print(tags)  # checking the tags left


''' Accessing the mxCell child nodes ##'''
# The aim is to access specific details of each mxCell child node to then formulate the conversion into watson compliant JSON ##
# I need to remove the initial 2 mxCell elements as they are just placeholders in DrawIO structure.
'''
# Firstly, return all mxCells:
for child in rootfinal:
    print(child.tag, child.attrib)
print("\n")
'''
for cell in rootfinal.findall('mxCell'):
    idx = int(cell.attrib.get("id"))  # apparently cell.attrib.get will be my bread and butter.
    if idx <= 1:
        rootfinal.remove(cell)
'''
# Check it worked/see all mxCells (drawio shapes)
for child in rootfinal:
    print(child.tag, child.attrib)
'''

# Look at most critical data points first now, we need style to determine what shape it is, value as the node title, and then visual representation source and target nodes.
'''
for child in rootfinal:
    Cellinfo = [child.attrib.get("value"), child.attrib.get("style"), child.attrib.get("source"),
                child.attrib.get("target")]
    print(Cellinfo)  # This shows us all the mxCell data we need.
'''
'''Extracting nodes based on style'''
# Seperate and extract the nodes based on "style", i.e. what they are meant to represent to the watson dev
# e.g. find all rounded and extract value, source and target
#       SIZE MATTERS (!) FOR SHAPES []
#       SIZE DOES NOT MATTER FOR ARROWS->
# for this to work, flawlessly during early stages, the size of ALL shapes need to be the same. Not just amongst each other, but in all diagrams.
# the size requirement is 1 box down, 3 across. FOR ALL SHAPES.

# I also need to create dictionaries containing all the relevant info

# Finding all nodes:
node_rectangles_list = []
node_circles_list = []
node_arrows_list = []
node_matching_list = []

for nodes in rootfinal.findall(".//mxCell"):
    # rectangles:
    if nodes.attrib["style"] == "rounded=0;whiteSpace=wrap;html=1;":
        node_rectangles = {'id': nodes.attrib.get('id'), 'title': nodes.attrib.get('value'),
                           'text': nodes.attrib.get('value'),
                           'selection_policy': "sequential", 'condition': ''}
        nodes_intermediary = nodes.attrib.get('value')
        if nodes.attrib.get('x') == 40 or nodes.attrib.get('value') == "welcome":
            node_rectangles['condition'] = ""
        elif "@" in nodes.attrib.get('value'):
            node_rectangles['condition'] = f"@{nodes_intermediary}"
        else:
            node_rectangles['condition'] = nodes_intermediary
        node_rectangles_list.append(node_rectangles)
    # circles
    if nodes.attrib["style"] == "ellipse;whiteSpace=wrap;html=1;aspect=fixed;":
        node_circles = {'id': nodes.attrib.get('id'), 'text': nodes.attrib.get('value')}
        node_circles_list.append(node_circles)
    # arrows
    if nodes.attrib[
        "style"] == "edgeStyle=none;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" or \
            nodes.attrib[
                "style"] == "edgeStyle=none;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;":
        node_arrows = {'id': nodes.attrib.get('id'), 'source': nodes.attrib.get('source'),
                       'target': nodes.attrib.get('target')}
        node_arrows_list.append(node_arrows)

nodes_matched = defaultdict(dict)
source_list = []
target_list = []
circle_list = []
arrow_link = {}

'IDENTIFYING TARGETS AND SOURCES'
for arrows in node_arrows_list:
    for nodes in node_rectangles_list:
        if arrows['source'] in nodes['id']:
            arrow_link = {'Arrow id': arrows['id'], 'Source Rectangle Title': nodes['title']}
            source_list.append(arrow_link)
        if arrows['target'] in nodes['id']:
            arrow_link = {'Arrow id': arrows['id'], 'Target Rectangle Title': nodes['title']}
            target_list.append(arrow_link)
    for nodes in node_circles_list:
        if arrows['target'] in nodes['id']:
            arrow_link = {'Arrow id': arrows['id'], 'Target Circle Text': nodes['text']}
            circle_list.append(arrow_link)


print("\n Rectangles: ")
for items in node_rectangles_list:
    print(f"Node ID: {items['id']} -> Node Title: {items['title']}")
print("\n Circles: ")
for items in node_circles_list:
    print(f"Node ID: {items['id']} -> Node Text: {items['text']}")
print("\n Arrows: ")
for items in node_arrows_list:
    print(f"Node ID: {items['id']} -> Node Source: {items['source']}-> Node Target: {items['target']}")

# Combining the arrows of each list, such that they can be matched:
for item in source_list + target_list + circle_list:
    nodes_matched[item['Arrow id']].update(item)
final_nodes = json.loads(json.dumps(nodes_matched))
#print(list(final_nodes.values()))


#mapping the arrows to each unique rectangle so that it can be extracted for the WA nodes:
dict_list = list(final_nodes.values())
final_nodes = list(map(lambda dict_tuple: dict(ChainMap(*dict_tuple[1])),
                       groupby(sorted(dict_list,
                                      key=lambda sub_dict: sub_dict["Source Rectangle Title"]),
                               key=lambda sub_dict: sub_dict["Source Rectangle Title"])))

for item in final_nodes:
    if 'Target Rectangle Title' in item:
        previous_sibling = item['Target Rectangle Title']
        item_to_be_changed = next(item for item in final_nodes if item["Source Rectangle Title"] == previous_sibling)
        item_to_be_changed['Previous Sibling'] = item['Source Rectangle Title']

# flesh out the final nodes with information from the node_rectangles list (can be more advanced later)
for item in final_nodes:
    item['selection_policy'] = "sequential"
    item['condition'] = ''
print("\n")
pprint(final_nodes)

'''Creating the conversions into Dialog JSON'''
'building the dialog nodes:'
nodes = []
counter = 1
for item in final_nodes:
    globals()[f"node_standard{counter}"] = {
        "type": "standard",
        "title": item['Source Rectangle Title'],
        "output": {
            "generic": [
                {
                    "values": [
                        {
                            "text": item['Target Circle Text']
                        }
                    ],
                    "response_type": "text",
                    "selection_policy": item['selection_policy']
                }
            ]
        },
        "conditions": item['condition'],
        "dialog_node": item['Source Rectangle Title'],
    }
    if item['Source Rectangle Title'] == 'welcome':
        del globals()[f'node_standard{counter}']['conditions']
    if 'Previous Sibling' in item:
        globals()[f'node_standard{counter}']['previous_sibling'] = item['Previous Sibling']
    nodes.append(globals()[f'node_standard{counter}'])
    counter = counter + 1


'''Compiling Dialog'''
path2 = os.getcwd()
file2 = "compiled_dialog.json"
filepath2 = path2 + "\\" + file2
print("\nSeeking intents dialog file...")
if os.path.isfile(filepath2) and os.access(filepath2, os.R_OK):
    print("Intents dialog JSON file found and is accessible.")
else:
    print("Files missing, creating new copies.")
    with io.open(os.path.join(path2, 'compiled_dialog.json'), 'w') as db_file2:
        db_file2.write(json.dumps({}))

with open("compiled_dialog.json", "w") as f:
    json.dump(nodes, f, indent=4)

'''Compiling Watson'''
path = os.getcwd()
file = "compiled_watson.json"
filepath = path + "\\" + file
print("\nSeeking Watson Compliant JSON...")
if os.path.isfile(filepath) and os.access(filepath, os.R_OK):
    print("Compiled Watson JSON found file found and is accessible.\n")
else:
    print("Files missing, creating new copies.")
    with io.open(os.path.join(path, 'compiled_watson.json'), 'w') as db_file:
        db_file.write(json.dumps({}))

# all JSON imports or construction here:
# entities
with open('entities_test_export.json') as json_file:
    json_entities = json.load(json_file)
# intents
with open('intents_test_export.json') as json_file:
    json_intents = json.load(json_file)
# metadata
json_meta = {"api_version": {"major_version": "v2", "minor_version": "2018-11-08"}}  # can make this modular

# dialogue
with open('compiled_dialog.json') as json_file:
    json_dia = json.load(json_file)

# counterexample
# remains as is for now.

# system settings
# this has an issue, true is replaced by 'true' in python. In json its just meant to be true without quotations.
json_settings = {"off_topic": {
    "enabled": True
},
    "disambiguation": {
        "prompt": "Did you mean:",
        "enabled": True,
        "randomize": True,
        "max_suggestions": 5,
        "suggestion_text_policy": "title",
        "none_of_the_above_prompt": "None of the above"
    },
    "human_agent_assist": {
        "prompt": "Did you mean:"
    },
    "intent_classification": {
        "training_backend_version": "v2"
    },
    "spelling_auto_correct": True
}

# name = input("What is the name of this skill?")
name = "Password Reset"

# description = input("Provide a brief description for this skill")
description = "Basic Password Reset Request"

final_details = {"learning_opt_out": False,
                 "name": name,
                 "language": "en",
                 "description": description}

final_json = {"intents": [json_intents], "entities": [json_entities], "metadata": json_meta, "dialog_nodes": json_dia,
              "counterexamples": [], "system_settings": json_settings}

for item in final_details:
    final_json[item] = final_details[item]
print(final_json)

with open("compiled_watson.json", "w") as f:
    json.dump(final_json, f, indent=4)
print("\nChanges were saved successfully!")
