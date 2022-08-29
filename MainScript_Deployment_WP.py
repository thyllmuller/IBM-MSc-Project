import io
import json
import os
import random
import re
import time
import xml.etree.ElementTree as ETx
from pprint import pprint

'''Reading in a sample XML'''
tree = ETx.parse("Watson_Pizzeria_Test.drawio")
root = tree.getroot()
xmlstr = ETx.tostring(root, encoding='unicode',
                      method='xml')  # unicode not utf-8
strx = """math="0" shadow="0">"""
pattern = "^[^³]*" + strx + "\n"  # will match all text until it finds the string (plus newline removal)
xmlstr = re.sub(pattern, '', xmlstr)

stry = "        </mxGraphModel>"
pattern = stry + "[^|]*$"
xmlstr = re.sub(pattern, '', xmlstr)

xmlfinal = ETx.ElementTree(ETx.fromstring(xmlstr))
rootfinal = xmlfinal.getroot()
tags = {elem.tag for elem in rootfinal.iter()}

# pattern = "^(.*)(?=<root)" # this is correct, but it doesn't work…presumably because of the way the parsing is done.
# xmlstr = re.sub("^(.*)(?=<root)", '', xmlstr)

''' Accessing the mxCell child nodes ##'''
# The aim is to access specific details of each mxCell child node to then formulate the conversion into watson compliant JSON ##
# I need to remove the initial 2 mxCell elements as they are just placeholders in DrawIO structure.

for cell in rootfinal.findall('mxCell'):
    idx = int(cell.attrib.get("id"))  # apparently cell.attrib.get will be my bread and butter.
    if idx <= 1:
        rootfinal.remove(cell)

# Look at most critical data points first now, we need style to determine what shape it is, value as the node title, and then visual representation source and target nodes.
''' saving this as a print verify
for child in rootfinal:
    Cellinfo = [child.attrib.get("value"), child.attrib.get("style"), child.attrib.get("source"),
                child.attrib.get("target")]
    print(Cellinfo)  # This shows us all the mxCell data we need.
'''

'Finding all nodes:'
'''Extracting nodes based on style'''
node_rectangles_list = []
node_circles_list = []
node_arrows_list = []
node_triangles_list = []
node_curves_list = []
node_matching_list = []
node_diamonds_list = []
node_hectagons_list = []
node_ellipses_list = []

'ALL shapes here because otherwise it gets messy'
rect1 = "rounded=0;whiteSpace=wrap;html=1;"
hex1 = "shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;fixedSize=1;fontFamily=Helvetica;fontSize=12;fontColor=rgb(240, 240, 240);align=center;strokeColor=rgb(240, 240, 240);fillColor=rgb(42, 42, 42);"
circ1 = "ellipse;whiteSpace=wrap;html=1;aspect=fixed;fontFamily=Helvetica;fontSize=12;fontColor=rgb(240, 240, 240);align=center;strokeColor=rgb(240, 240, 240);fillColor=rgb(42, 42, 42);"
tri1 = "triangle;whiteSpace=wrap;html=1;"
dia1 = "rhombus;whiteSpace=wrap;html=1;"
arrow1 = "edgeStyle=none;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;"
arrow2 = "edgeStyle=none;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;"
arrow3 = "edgeStyle=none;html=1;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;"
curve1 = "curved=1;endArrow=classic;html=1;fontFamily=Helvetica;fontSize=11;fontColor=rgb(240, 240, 240);align=center;strokeColor=rgb(240, 240, 240);"
elip1 = "ellipse;whiteSpace=wrap;html=1;"

for nodes in rootfinal.findall(".//mxCell"):
    # rectangles:
    if nodes.attrib["style"] == rect1 or nodes.attrib['style'] == hex1:
        node_rectangles = {'id': nodes.attrib.get('id'), 'title': nodes.attrib.get('value'),
                           'text': nodes.attrib.get('value')}
        node_rectangles_list.append(node_rectangles)
    # circles
    if nodes.attrib["style"] == circ1:
        node_circles = {'id': nodes.attrib.get('id'), 'text': nodes.attrib.get('value')}
        node_circles_list.append(node_circles)
    # arrows
    if nodes.attrib["style"] == arrow1 or nodes.attrib["style"] == arrow2 or nodes.attrib["style"] == arrow3:
        node_arrows = {'id': nodes.attrib.get('id'), 'source': nodes.attrib.get('source'),
                       'target': nodes.attrib.get('target')}
        node_arrows_list.append(node_arrows)
    # triangles
    if nodes.attrib["style"] == tri1:
        node_triangles = {'id': nodes.attrib.get('id'), 'text': nodes.attrib.get('value')}
        node_triangles_list.append(node_triangles)
    # reset curves
    if nodes.attrib["style"] == curve1:
        node_curves = {'id': nodes.attrib.get('id'), 'source': nodes.attrib.get('source'),
                       'target': nodes.attrib.get('target')}
        node_curves_list.append(node_curves)
    # event handler diamonds
    if nodes.attrib['style'] == dia1:
        node_diamonds = {'id': nodes.attrib.get('id'), 'event': nodes.attrib.get('value')}
        node_diamonds_list.append(node_diamonds)
    # slot hectagons
    if nodes.attrib['style'] == hex1:
        node_hectagons = {'id': nodes.attrib.get('id'), 'text': nodes.attrib.get('value')}
        node_hectagons_list.append(node_hectagons)
    # event_text ellipses
    if nodes.attrib['style'] == elip1:
        node_ellipses = {'id': nodes.attrib.get('id'), 'text': nodes.attrib.get('value')}
        node_ellipses_list.append(node_ellipses)

print("\033[4m" + "\nRectangles (including hectagons):" + "\033[0m")
for items in node_rectangles_list:
    print(f"Node ID: {items['id']} -> Node Title: {items['title']}")
print("\033[4m" + "\nCircles:" + "\033[0m")
for items in node_circles_list:
    print(f"Node ID: {items['id']} -> Node Text: {items['text']}")
print("\033[4m" + "\nTriangles (conditions):" + "\033[0m")
for items in node_triangles_list:
    print(f"Node ID: {items['id']} -> Node Text: {items['text']}")
print("\033[4m" + "\nDiamonds (events):" + "\033[0m")
for items in node_diamonds_list:
    print(f"Node ID: {items['id']} -> Node Text: {items['event']}")
print("\033[4m" + "\nArrows:" + "\033[0m")
for items in node_arrows_list:
    print(f"Arrow ID: {items['id']} -> Node Source: {items['source']}-> Node Target: {items['target']}")
print("\033[4m" + "\nCurves:" + "\033[0m")
for items in node_curves_list:
    print(f"Curve Arrow ID: {items['id']} -> Node Source: {items['source']}-> Node Target: {items['target']}")
print("\033[4m" + "\nHectagons (slots):" + "\033[0m")
for items in node_hectagons_list:
    print(f"Hectagon ID: {items['id']} -> Node Text: {items['text']}")
print("\033[4m" + "\nEllipses (event texts):" + "\033[0m")
for items in node_ellipses_list:
    print(f"Ellipse ID: {items['id']} -> Node Text: {items['text']}")

'Identifying the targets and sources of all arrows'
node_list = []
arrow_targets = []
for node in node_rectangles_list:
    arrow_targets = []
    for arrow in node_arrows_list:
        if node['id'] in arrow['source']:
            arrow_target = arrow['target']
            arrow_targets.append(arrow_target)
    arrow_target_list = {"Node ID": node['id'], "Node Title": node['title'], "Node Targets": arrow_targets}
    node_list.append(arrow_target_list)
node_details_list = []

for nodes in node_list:
    node_details = {'node title': nodes['Node Title'], 'node id': nodes['Node ID']}
    for node in nodes['Node Targets']:
        # rectangles
        for item in node_rectangles_list:
            if item['id'] == str(node):
                node_details['target_rect'] = item['text']
        # circles
        for item in node_circles_list:
            if item['id'] == str(node):
                node_details['text'] = item['text']
        # triangles
        for item in node_triangles_list:
            if item['id'] == str(node):
                node_details['conditions'] = item['text']
        # diamonds
        for item in node_diamonds_list:
            if item['id'] == str(node):
                node_details['event'] = item['event']
        # curves
        for item in node_curves_list:
            if item['source'] == nodes['Node ID']:
                temp_item = next(rect for rect in node_rectangles_list if rect['id'] == item['target'])
                node_details['next_step'] = {"behavior": "jump_to", "selector": "body",
                                             # only capable of "jump_to" currently
                                             "dialog_node": temp_item[
                                                 'title']}  # only capable of selecting a body target, assuming this is depedent on child nodes etc
    node_details_list.append(node_details)

'Fixing text for event_handler diamonds'
for item in node_diamonds_list:
    arrow_match = next(arro for arro in node_arrows_list if arro['source'] == item['id'])
    eli_match = next(eli for eli in node_ellipses_list if eli['id'] == arrow_match['target'])
    prev_arrow = next(arro for arro in node_arrows_list if arro['target'] == item['id'])
    prev_source = next(rect for rect in node_details_list if rect['node id'] == prev_arrow['source'])
    prev_source['event_text'] = eli_match['text']

'Adding slot by identification via if object was hectagon'
for item in node_hectagons_list:
    for rect in node_rectangles_list:
        if item['id'] == rect['id']:
            temp_item = next(node for node in node_details_list if node['node id'] == item['id'])
            temp_item['slot'] = True

'Adding parent node to overall details and...'
'Adding extra hardcoded information that can be expanded on in the future, also adding in current contingency'
for item in node_details_list:
    if 'target_rect' in item:
        next_rect = item['target_rect']
        temp_item = next(item for item in node_details_list if item["node title"] == next_rect)
        temp_item['previous_sibling'] = item['node title']
    item['selection_policy'] = "sequential"
    if 'text' not in item:  # contingency for text currently
        item['text'] = ""
'''Creating the conversions into Dialog JSON'''
'Building the STANDARD dialog nodes:'
nodes = []
print("\033[4m" + "\nCommencing node building..." + "\033[0m")
print("\nNow building Standard Nodes...")
time.sleep(1)
for index, item in enumerate(node_details_list):
    globals()[f"node_standard{index + 1}"] = {
        "type": "standard",
        "title": item['node title'],
        "output": {
            "generic": [
                {
                    "values": [
                        {
                            "text": item['text']
                        }
                    ],
                    "response_type": "text",
                    "selection_policy": item['selection_policy']
                }
            ]
        },
        "conditions": item['conditions'],
        "dialog_node": item['node title'],
    }
    if 'next_step' in item:
        print("\nNext_Step located in node: " + item['node title'])
        print("Please verify..")
        verify_context_dismissal = input("Do you want this next_step:jump to also clear context variables?(Y/N): ")
        if verify_context_dismissal == "y" or verify_context_dismissal == "Y":
            counter_internal = int(input("How many are being reset? "))
            context_dict = {}
            for i in range(counter_internal):
                vari_reset = input(
                    "Type the context variable exactly as it would appear in Watson Assistant, then press enter: ")
                new_entry = {vari_reset: None}
                context_dict[vari_reset] = None
            globals()[f'node_standard{index + 1}']['context'] = context_dict
        globals()[f'node_standard{index + 1}']['next_step'] = item['next_step']
    if 'previous_sibling' in item:
        globals()[f'node_standard{index + 1}']['previous_sibling'] = item['previous_sibling']
    if item['node title'] == 'welcome':
        # del globals()[f'node_standard{index + 1}']['conditions'] maybe not needed
        del globals()[f'node_standard{index + 1}']['previous_sibling']  # contingency
    if 'slot' in item:
        globals()[f'node_standard{index + 1}']['slot'] = True
    if 'event' in item:
        globals()[f'node_standard{index + 1}']['event'] = True
    if item['conditions'] == '#anything_else':
        digressionsprompt = input(
            "\nA fallback node has been identified, would you like to disable inward digressions but enable outward digressions (Y/N)? ")
        if digressionsprompt == "y" or digressionsprompt == "Y":
            globals()[f'node_standard{index + 1}']['digress_in'] = 'not_available'
            globals()[f'node_standard{index + 1}']['digress_out'] = 'allow_all'
    nodes.append(globals()[f'node_standard{index + 1}'])

'Addition of Event Handlers'
print("\nNow building Event Handlers...")
time.sleep(1)
total_events = 0
for item in nodes:
    if 'event' in item:
        total_events = total_events + 1
event_ids = random.sample(range(1000000000000, 2000000000000), total_events)
temp_text = ""
for index, item in enumerate(nodes):
    if 'event' in item:
        verify_slot = item['title']
        for node in node_details_list:
            if node['node title'] == item['title']:
                temp_text = node['event_text']
        temp_item = next(item for item in nodes if item['title'] == verify_slot)
        new_event = {
            "type": "event_handler",
            "output": {
                "text": {
                    "values": [temp_text]  # ask jacob about this
                }
            },
            "parent": temp_item['title'],
            "metadata": {},
            "conditions": temp_item['conditions'],
            "event_name": "generic",
            "dialog_node": f"handler_{index}_{event_ids[index - 1]}"}
        temp_item = next(item for item in node_details_list if item['node title'] == verify_slot)
        new_event['conditions'] = temp_item['event']
        nodes.append(new_event)

'Conversion to Slot Frame'
print("\nNow converting respective slot nodes...")
time.sleep(1)
new_slot = {}
for item in nodes:
    if 'slot' in item:
        verify_slot = item['title']
        temp_item = next(item for item in nodes if item['title'] == verify_slot)
        new_slot = {
            "type": "frame",
            "title": temp_item['title'],
            "output": {},
            "metadata": {
                "fallback": "leave"
            },
            "conditions": temp_item['conditions'],
            "digress_in": "does_not_return",
            "dialog_node": temp_item['title'],
            "digress_out": "allow_all",
            "previous_sibling": temp_item['previous_sibling'],
            "digress_out_slots": "allow_all"}
        for i in range((len(nodes)) - 1):
            if 'title' in nodes[i] and nodes[i]['title'] == temp_item['title']:
                del nodes[i]
        nodes.append(new_slot)

print("\n" + "\033[4m" + "\nAll nodes successfully built:" + "\033[0m")
for index, item in enumerate(nodes):
    print("\033[4m" + f"\nNode {index + 1}:" + "\033[0m" + " " + item['dialog_node'])
    pprint(item)

'''Compiling Dialog from the nodes'''
'Creating the JSON File or overwriting the existing one'
path2 = os.getcwd()
file2 = "compiled_dialog.json"
filepath2 = path2 + "\\" + file2
print("\nSeeking dialog file...")
if os.path.isfile(filepath2) and os.access(filepath2, os.R_OK):
    print("Dialog JSON file found and is accessible.")
else:
    print("Files missing, creating new copies.")
    with io.open(os.path.join(path2, 'compiled_dialog.json'), 'w') as db_file2:
        db_file2.write(json.dumps({}))

'Writing nodes into json file'
with open("compiled_dialog.json", "w") as f:
    json.dump(nodes, f, indent=4)

'''Compiling Watson from all objects'''
'Creating the Watson JSON File or overwriting the existing one'
path = os.getcwd()
file = "compiled_watson_wp.json"
filepath = path + "\\" + file
print("\nSeeking Watson Compliant JSON...")
if os.path.isfile(filepath) and os.access(filepath, os.R_OK):
    print("Compiled Watson JSON found file found and is accessible.\n")
else:
    print("Files missing, creating new copies.")
    with io.open(os.path.join(path, 'compiled_watson_wp.json'), 'w') as db_file:
        db_file.write(json.dumps({}))

'Loading entities from catalogue export'
with open('entities_test_export_wp.json') as json_file:
    json_entities = json.load(json_file)

'Loading intents from catalogue export'
with open('intents_test_export_wp.json') as json_file:
    json_intents = json.load(json_file)

'Hardcoding the json_meta data within the watson configs at the end of the JSON file'
json_meta = {"api_version": {"major_version": "v2", "minor_version": "2018-11-08"}}  # can make this modular

'Loading in the dialogue we created above'
with open('compiled_dialog.json') as json_file:
    json_dia = json.load(json_file)

'Counterexample'
# remains as is for now. future work can tackle this

'System Settings'
# This had an issue with the True parameter being different between python and json, but it is fixed for now
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

'Skill Name'
# name = input("What is the name of this skill?")
name = "Watson Pizzeria"

'Skill Description'
# description = input("Provide a brief description for this skill")
description = "Pizzeria order virtual bot - test deployment"

'Final Details'
final_details = {"learning_opt_out": False,
                 "name": name,
                 "language": "en",
                 "description": description}

'Constructing the final JSON from all of the objects created'
'One minor point - if only a SINGLE intent or entity is part of the catalogue -> you must add [] to it in the next line!'
final_json = {"intents": json_intents, "entities": json_entities, "metadata": json_meta, "dialog_nodes": json_dia,
              "counterexamples": [], "system_settings": json_settings}
for item in final_details:
    final_json[item] = final_details[
        item]  # redudant now, you can make this final_json['final_details'] = final_details

with open("compiled_watson_wp.json", "w") as f:
    json.dump(final_json, f, indent=4)
print("\nFinal export was saved as 'compiled_watson_wp.json' !")
