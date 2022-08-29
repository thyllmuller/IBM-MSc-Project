import io
import json
import os
import re


# Get the JSON ready
def InitialiseJSON():
    path = os.getcwd()
    file = "entities_test_export_wp.json"
    filepath = path + "\\" + file
    print("\nInitialising system files.")
    if os.path.isfile(filepath) and os.access(filepath, os.R_OK):
        print("JSON entities file found and is accessible.")
    else:
        print("Files missing, creating new copies.")
        with io.open(os.path.join(path, 'entities_test_export_wp.json'), 'w') as db_file:
            db_file.write(json.dumps({}))


# Starting my App.
InitialiseJSON()


# Creating a catalogue:
def initialise_catalogue():
    with open("entities_test_export_wp.json", "r") as fp:
        data = json.load(fp)
    return data


def is_number(value):  # might not need this
    try:
        var = float(value)
        return True
    except (TypeError, ValueError):
        return False


# Conversion of set to list. --might not need
def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


# list all entities
def show_all_entities(placeholder):
    print("\nShowing all entities.....")
    for dictx in catalogue:
        idx, entity = dictx["ID"], dictx["entity"]
        print(f"Code: {idx} --->   Entity: {entity}")


# list all details for an entity
def entity_detail(placeholder):
    print("\nView details of an entity.....")
    code = code_input()
    entity_item = next(item for item in catalogue if item[
        "ID"] == code)  # https://peps.python.org/pep-0289/ #Generator expressions are especially useful with functions like sum(), min(), and max() that reduce an iterable input to a single value:
    # idsum = sum(dictsum.get('ID') == "K" for dictsum in catalogue) useful for lookup!
    # or sum(item['ID'] for item in catalogue)
    # or len([item for item in obj if isinstance(item, dict)])
    # print(idsum)
    print(entity_item)  # can create if else loop for the cases where someone mistypes the entity code


# Create an entity
def create_entity(placeholder):
    global catalogue
    print("\nTo add a new entity to the list, please adhere to the formatting requirements.")
    print("(Bear in mind, advanced changes can still be made from within the Watson Assistant)")
    entry_name = input(
        "Using only lowercase letters and replacing spaces with underscores, please specify the name now: ")
    value = ""
    if len(catalogue) == 0:
        new_id = 1
        catalogue = {"ID": f"K{new_id}", "entity": f"{entry_name}", "values": []}
        value_count = int(input("\nHow many values will this entity contain?\nTotal number of values: "))
        for i in range(value_count):
            globals()[f"valuex_dict{i}"] = {"type": "synonyms", "value": f"{value}", "synonyms": []}
            value_input = input(f"\nValue {i + 1}: ")
            print(f"Please provide two synonyms for {value_input}:")
            for x in range(2):
                syn = input(f"Synonym {x + 1}: ")
                globals()[f"valuex_dict{i}"]["synonyms"].append(syn)
            globals()[f"valuex_dict{i}"]["value"] = value_input
            catalogue["values"].append(globals()[f"valuex_dict{i}"])
        obj = [catalogue]
        with open("new_entities.json", "w") as f:
            json.dump(obj, f, indent=4)
    else:
        new_id = int(len(catalogue) + 1)
        code = f"K{new_id}"
        new_dict = {"ID": f"K{new_id}", "entity": f"{entry_name}", "values": []}
        catalogue.append(new_dict)
        entity_item = next(item for item in catalogue if item["ID"] == code)
        value_count = int(input("\nHow many values will this entity contain?\nTotal number of values: "))
        for i in range(value_count):
            globals()[f"valuex_dict{i}"] = {"type": "synonyms", "value": f"{value}", "synonyms": []}
            value_input = input(f"\nValue {i + 1}: ")
            print(f"Please provide two synonyms for {value_input}:")
            for x in range(2):
                syn = input(f"Synonym {x + 1}: ")
                globals()[f"valuex_dict{i}"]["synonyms"].append(syn)
            globals()[f"valuex_dict{i}"]["value"] = value_input
            entity_item["values"].append(globals()[f"valuex_dict{i}"])
        save_entities(placeholder)


# Change the name of an entity
def change_entity_name(placeholder):
    code = code_input()
    entity_item = next(item for item in catalogue if item["ID"] == code)
    print(f"""\nCurrent entity name is "{entity_item["entity"]}" """)
    entity_item["entity"] = input("Please type the new name now: ")
    print(f"\nYou have successfully edited the entity name. The updated name now reads:\n{entity_item['entity']}")
    save_entities(placeholder)


# Update entity synonyms
def edit_entity(placeholder):
    update_counter = 1
    code = code_input()
    entity_item = next(item for item in catalogue if item["ID"] == code)
    print(f"\nYou have selected the '{entity_item['entity']}' entity.")
    for entity in range(len(entity_item["values"])):
        print(f"Value number ({update_counter}) -> {entity_item['values'][entity]['value']}")
        update_counter = update_counter + 1
    entity_selected = int(input("\nFor which value do you want to edit the synonyms?: "))
    if entity_selected > len(entity_item["values"]):  # if they pick 2x wrong numbers it breaks
        entity_selected = int(input("\nNo entity was found with that number, please specify entity number again: "))
        entity_selected = entity_selected - 1
        print(f"\nEntity selected: {entity_item['values'][entity_selected]['value']}")
        counter_syn = 1
        for item in range(len(entity_item['values'][entity_selected]['synonyms'])):
            print(f"Synonym number ({counter_syn}) -> {entity_item['values'][entity_selected]['synonyms'][item]}")
            counter_syn = counter_syn + 1
        synonym_selected = int(input("\nWhich entity synonym do you want to edit, synonym number:")) - 1
        entity_item['values'][entity_selected]['synonyms'][synonym_selected] = input(
            f"\nPlease type the updated synonym now:")
        print(
            f"\nYou have successfully edited the synonym. The updated synonym now reads:\n'{entity_item['values'][entity_selected]['synonyms'][synonym_selected]}'")
        save_entities(placeholder)
    elif entity_selected <= 0:
        entity_selected = int(input("\nNo entity was found with that number, please specify entity number again: "))
        entity_selected = entity_selected - 1
        print(f"\nEntity selected: {entity_item['values'][entity_selected]['value']}")
        counter_syn = 1
        for item in range(len(entity_item['values'][entity_selected]['synonyms'])):
            print(f"Synonym number ({counter_syn}) -> {entity_item['values'][entity_selected]['synonyms'][item]}")
            counter_syn = counter_syn + 1
        synonym_selected = int(input("\nWhich entity synonym do you want to edit, synonym number:")) - 1
        entity_item['values'][entity_selected]['synonyms'][synonym_selected] = input(
            f"\nPlease type the updated synonym now:")
        print(
            f"\nYou have successfully edited the synonym. The updated synonym now reads:\n'{entity_item['values'][entity_selected]['synonyms'][synonym_selected]}'")
        save_entities(placeholder)
    else:
        entity_selected = entity_selected - 1
        print(f"\nEntity selected: {entity_item['values'][entity_selected]['value']}")
        counter_syn = 1
        for item in range(len(entity_item['values'][entity_selected]['synonyms'])):
            print(f"Synonym number ({counter_syn}) -> {entity_item['values'][entity_selected]['synonyms'][item]}")
            counter_syn = counter_syn + 1
        synonym_selected = int(input("\nWhich entity synonym do you want to edit, synonym number:")) - 1
        entity_item['values'][entity_selected]['synonyms'][synonym_selected] = input(
            f"\nPlease type the updated synonym now:")
        print(
            f"\nYou have successfully edited the synonym. The updated synonym now reads:\n'{entity_item['values'][entity_selected]['synonyms'][synonym_selected]}'")
        save_entities(placeholder)


# Add a synonym to an entity
def add_synonym(placeholder):
    code = code_input()
    entity_item = next(item for item in catalogue if item["ID"] == code)
    print(f"\nCurrent selected entity is '{entity_item['entity']}'.")
    print("It contains the following values:")
    add_counter = 1
    for entity in range(len(entity_item["values"])):
        print(f"    Value number ({add_counter}) -> {entity_item['values'][entity]['value']}")
        add_counter = add_counter + 1
    value_selected = int(input("\nFor which value do you want to edit the synonyms?: "))
    if value_selected > len(entity_item["values"]):  # if they pick 2x wrong numbers it breaks
        value_selected = int(input("\nNo entity was found with that number, please specify entity number again: "))
        value_selected = value_selected - 1
        print(f"\nValue selected: {entity_item['values'][value_selected]['value']}")
        print_check = input(
            "Do you want to see all synonyms for this value(Y/N)?")  # (I don't know about this rn need to check) will also trigger if only 1 synonym AFTER deletion of ALL others - no issue here, just means 1 extra button for user to press.
        if print_check == "Y" or print_check == "y":
            counter_syn = 1
            for item in range(len(entity_item['values'][value_selected]['synonyms'])):
                print(f"Synonym number ({counter_syn}) -> {entity_item['values'][value_selected]['synonyms'][item]}")
                counter_syn = counter_syn + 1
        new_synonym = input("Enter new synonym: ")
        entity_item['values'][value_selected]['synonyms'].append(new_synonym)
    elif value_selected <= 0:
        value_selected = int(input("\nNo entity was found with that number, please specify entity number again: "))
        value_selected = value_selected - 1
        print(f"\nValue selected: {entity_item['values'][value_selected]['value']}")
        print_check = input(
            "Do you want to see all synonyms for this value(Y/N)?")  # (I don't know about this rn need to check) will also trigger if only 1 synonym AFTER deletion of ALL others - no issue here, just means 1 extra button for user to press.
        if print_check == "Y" or print_check == "y":
            counter_syn = 1
            for item in range(len(entity_item['values'][value_selected]['synonyms'])):
                print(f"Synonym number ({counter_syn}) -> {entity_item['values'][value_selected]['synonyms'][item]}")
                counter_syn = counter_syn + 1
        new_synonym = input("Enter new synonym: ")
        entity_item['values'][value_selected]['synonyms'].append(new_synonym)
    else:
        value_selected = value_selected - 1
        print(f"\nValue selected: {entity_item['values'][value_selected]['value']}")
        print_check = input(
            "Do you want to see all synonyms for this value(Y/N)?")  # (I don't know about this rn need to check) will also trigger if only 1 synonym AFTER deletion of ALL others - no issue here, just means 1 extra button for user to press.
        if print_check == "Y" or print_check == "y":
            counter_syn = 1
            for item in range(len(entity_item['values'][value_selected]['synonyms'])):
                print(f"Synonym number ({counter_syn}) -> {entity_item['values'][value_selected]['synonyms'][item]}")
                counter_syn = counter_syn + 1
        new_synonym = input("Enter new synonym: ")
        entity_item['values'][value_selected]['synonyms'].append(new_synonym)
    save_entities(placeholder)


# Remove a synonym from an entity
def remove_synonym(placeholder):
    code = code_input()
    entity_item = next(item for item in catalogue if item["ID"] == code)
    print(f"\nCurrent selected entity is '{entity_item['entity']}'.")
    print("It contains the following values:")
    add_counter = 1
    for entity in range(len(entity_item["values"])):
        print(f"    Value number ({add_counter}) -> {entity_item['values'][entity]['value']}")
        add_counter = add_counter + 1
    value_selected = int(input("\nFor which value do you want to edit the synonyms?: "))
    if value_selected > len(entity_item["values"]):  # if they pick 2x wrong numbers it breaks
        value_selected = int(input("\nNo entity was found with that number, please specify entity number again: "))
        value_selected = value_selected - 1
        print(f"\nValue selected: {entity_item['values'][value_selected]['value']}")
        print_check = input(
            "Do you want to see all synonyms for this value(Y/N)?")  # (I don't know about this rn need to check) will also trigger if only 1 synonym AFTER deletion of ALL others - no issue here, just means 1 extra button for user to press.
        if print_check == "Y" or print_check == "y":
            counter_syn = 1
            for item in range(len(entity_item['values'][value_selected]['synonyms'])):
                print(f"Synonym number ({counter_syn}) -> {entity_item['values'][value_selected]['synonyms'][item]}")
                counter_syn = counter_syn + 1
        synonym_selected = int(input("\nWhich entity synonym do you want to delete, synonym number:")) - 1
        del_check = input("Are you sure you want to delete this synonym(Y/N)?")
        if del_check == "Y" or del_check == "y":
            del entity_item["synonyms"][synonym_selected]
    elif value_selected <= 0:
        value_selected = int(input("\nNo entity was found with that number, please specify entity number again: "))
        value_selected = value_selected - 1
        print(f"\nValue selected: {entity_item['values'][value_selected]['value']}")
        print_check = input(
            "Do you want to see all synonyms for this value(Y/N)?")  # (I don't know about this rn need to check) will also trigger if only 1 synonym AFTER deletion of ALL others - no issue here, just means 1 extra button for user to press.
        if print_check == "Y" or print_check == "y":
            counter_syn = 1
            for item in range(len(entity_item['values'][value_selected]['synonyms'])):
                print(f"Synonym number ({counter_syn}) -> {entity_item['values'][value_selected]['synonyms'][item]}")
                counter_syn = counter_syn + 1
        synonym_selected = int(input("\nWhich entity synonym do you want to delete, synonym number:")) - 1
        del_check = input("Are you sure you want to delete this synonym(Y/N)?")
        if del_check == "Y" or del_check == "y":
            del entity_item["synonyms"][synonym_selected]
    else:
        value_selected = value_selected - 1
        print(f"\nValue selected: {entity_item['values'][value_selected]['value']}")
        print_check = input(
            "Do you want to see all synonyms for this value(Y/N)?")  # (I don't know about this rn need to check) will also trigger if only 1 synonym AFTER deletion of ALL others - no issue here, just means 1 extra button for user to press.
        if print_check == "Y" or print_check == "y":
            counter_syn = 1
            for item in range(len(entity_item['values'][value_selected]['synonyms'])):
                print(f"Synonym number ({counter_syn}) -> {entity_item['values'][value_selected]['synonyms'][item]}")
                counter_syn = counter_syn + 1
        synonym_selected = int(input("\nWhich entity synonym do you want to delete, synonym number:")) - 1
        del_check = input("Are you sure you want to delete this synonym(Y/N)?")
        if del_check == "Y" or del_check == "y":
            del entity_item['values'][value_selected]['synonyms'][synonym_selected]
    save_entities(placeholder)


# Save entities to new JSON
def save_prompt(placeholder):
    print("\nTo save your new file, please only use lowercase letters, numbers and spaces(or underscores).")
    save_changes = input(f"\nWhat should the name of the new file be?")
    with open(f"{save_changes}.json", "w") as f:
        json.dump(catalogue, f, indent=4)
    print("\nChanges were saved successfully!")


# Save entities continuously to JSON (as backup)
def save_entities(placeholder):
    with open("entity_list_test.json", "w") as f:
        json.dump(catalogue, f, indent=4)
    print("\nChanges were saved successfully!")
    # with open('data.json', 'w', encoding='utf-8') as f:
    # json.dump(data, f, ensure_ascii=False, indent=4)
    # there might be reason to use these later, if there are issues with encoding between the XML and the JSON - look here first


def code_input():
    code = input("Enter entity code: ")
    lc = re.compile("[a-z]+")
    low_k = lc.findall(code)
    if low_k == ["k"]:
        code = "K" + code[1]
    return code


# start main program
catalogue = initialise_catalogue()
print("\nWelcome to the entity catalogue")
print("-------------------------------\n")
while True:
    # Print out the menu:
    print("Please select an option :")
    print("1  List entities")
    print("2  View entity details")
    print("3  Create new entity")
    print("4  Update the name of an entity")
    print("5  Update existing entity synonyms")
    print("6  Add a synonym to an entity")
    print("7  Remove a synonym from an entity")
    print("S  Save all changes to a new file")
    print("W  Serialise for Export to Watson VA")
    print("X  Exit")

    # Get the user's choice:
    choice = input("> ")
    # Carry out task:
    if choice == '1':
        show_all_entities(catalogue)
    elif choice == '2':
        entity_detail(catalogue)
    elif choice == '3':
        create_entity(catalogue)
    elif choice == '4':
        change_entity_name(catalogue)
    elif choice == '5':
        edit_entity(catalogue)
    elif choice == '6':
        add_synonym(catalogue)
    elif choice == '7':
        remove_synonym(catalogue)
    elif choice == 'S' or choice == 's':
        save_prompt(catalogue)
    elif choice == 'X' or choice == 'x':
        print("Bye")
        break
    else:
        print("Invalid choice")
    print()
