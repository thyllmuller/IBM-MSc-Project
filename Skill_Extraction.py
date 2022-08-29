import json
import os
from pprint import pprint


'Seeking correct JSON'
path = os.getcwd()
while True:
    try:
        # file = input("\nWhat is the name of the Watson Assistant Skill file: ")
        file = "compiled_watson_wp.json"  # remove
        filepath = path + "\\" + file
        if os.path.isfile(filepath) and os.access(filepath, os.R_OK):
            print("Dialog JSON file found and is accessible.")
            with open(file) as json_file:
                skill = json.load(json_file)
            break
        else:
            print("File missing. Please try again.")
    except IOError:
        print("Invalid directory or read/write error.")

skill_nodes = skill["dialog_nodes"]
print("\nThis dialog skill contains the following nodes:")
for index, item in enumerate(skill_nodes):
    pprint(f"Node number {index + 1} --> {item['dialog_node']}")
print("\033[4m" + "Please bear in mind these are not sorted as they would be in Watson Assistant" + "\033[0m")

print("\nPlease select the node from which you want to create a branch:")
# select_node = input("Node name: ")
select_node = "Reset"  # remove

print("\nYou have selected the following node:")
grand_parent = next(node for node in skill["dialog_nodes"] if node['dialog_node'] == select_node)
print(grand_parent["dialog_node"])

print(
    "\nBranching will occur from this node (inclusive of the selected node) and iterate until all nodes are exhausted.")
# proceed = input("Proceed (Y/N)? ")
proceed = "y"  # remove

new_list = [grand_parent]
if proceed == "y" or proceed == "Y":
    for item in skill_nodes:
        if item["dialog_node"] == "welcome" or item["dialog_node"] == "Welcome":
            item["previous_sibling"] = None
            item["parent"] = None
        elif "parent" in item:
            item["previous_sibling"] = None
        elif "previous_sibling" in item:
            item["parent"] = None
    new_item = grand_parent
    for index, item in enumerate(skill_nodes):
        if item['previous_sibling'] is None and item['parent'] is None:
            continue
        else:
            if item['type'] == 'event_handler':
                for items in new_list:
                    if items['dialog_node'] == item['parent']:
                        new_list.append(item)
            else:
                for items in new_list:
                    if items['dialog_node'] == item['previous_sibling']:
                        new_list.append(item)


final_list = []
for index, item in enumerate(new_list):
    if item not in final_list:
        final_list.append(item)

#skill_to_be_modified = input("Please type the name of the skill you want to append the current nodes to (including the '.json' extension in the name): ")
skill_to_be_modified = "compiled_watson_wp_testappend.json"
with open(skill_to_be_modified) as json_file:
    json_skill_to_be_modified = json.load(json_file)
for item in final_list:
    json_skill_to_be_modified['dialog_nodes'].append(item)
#pprint(json_skill_to_be_modified['dialog_nodes'])

#new_name = input("Please type the name that you want the new file to have: ")
new_name = "compiled_watson_wp_append_final"
with open(f"{new_name}.json", "w") as f:
    json.dump(json_skill_to_be_modified, f, indent=4)
print(f"\nFinal export was saved as '{new_name}.json' !")

