import io
import json
import os
import re


# Get the JSON ready
def InitialiseJSON():
    path = os.getcwd()
    file = "intent_list_test.json"
    filepath = path + "\\" + file
    print("\nInitialising system files.")
    if os.path.isfile(filepath) and os.access(filepath, os.R_OK):
        print("JSON intents file found and is accessible.")
    else:
        print("Files missing, creating new copies.")
        with io.open(os.path.join(path, 'intent_list_test.json'), 'w') as db_file:
            db_file.write(json.dumps({}))


# Starting my App.
InitialiseJSON()


# Creating a catalogue:
def initialise_catalogue():
    with open("intent_list_test.json", "r") as fp:
        data = json.load(fp)
    return data


def is_number(value):  # might not need this
    try:
        var = float(value)
        return True
    except (TypeError, ValueError):
        return False


# List intents
def show_all_intents(catalogue):
    print("\nShowing all intents.....")
    for dictx in catalogue:
        idx, intentx = dictx["ID"], dictx["intent"]
        print(f"Code: {idx} --->   intent: {intentx}")


# View intent details
def intent_detail(catalogue):
    print("\nView details of an intent.....")
    code = code_input()
    intent_item = next(item for item in catalogue if item[
        "ID"] == code)  # https://peps.python.org/pep-0289/ #Generator expressions are especially useful with functions like sum(), min(), and max() that reduce an iterable input to a single value:
    # idsum = sum(dictsum.get('ID') == "G" for dictsum in catalogue) useful for lookup!
    # or sum(item['ID'] for item in catalogue)
    # or len([item for item in obj if isinstance(item, dict)])
    # print(idsum)
    print(intent_item)  # can create if else loop for the cases where someone mistypes the intent code


# Create new intent
def create_intent(catalogue):
    #global catalogue
    print("\nTo add a new intent to the list, please adhere to the formatting requirements.")
    print("(Bear in mind, advanced changes can still be made from within the Watson Assistant)")
    entry_name = input(
        "Using only lowercase letters and replacing spaces with underscores, please specify the name now: ")
    if len(catalogue) == 0:
        new_id = 1
    elif len(catalogue) == 3 and isinstance(catalogue, dict):
        new_id = 2
    else:
        new_id = int(len(catalogue) + 1)
    new_dict = {"ID": f"G{new_id}", "intent": f"{entry_name}", "examples": []}
    print(f"\nPlease provide two examples for the new intent '{entry_name}'.")
    if new_id == 1:
        for x in range(2):
            exam = input(f"Example {x + 1}: ")
            exam_dict = {"text": exam}
            new_dict["examples"].append(exam_dict)
        catalogue.update(new_dict)
        obj = [catalogue]
        with open("new_intents.json", "w") as f:
            json.dump(obj, f, indent=4)
        print("\nChanges were saved successfully!")
    elif new_id == 2:
        if "obj" in locals() or globals():
            catalogue = [catalogue]
        else:
            catalogue = catalogue
        for x in range(2):
            exam = input(f"Example {x + 1}: ")
            exam_dict = {"text": exam}
            new_dict["examples"].append(exam_dict)
        catalogue.append(new_dict)
    else:
        for x in range(2):
            exam = input(f"Example {x + 1}: ")
            exam_dict = {"text": exam}
            new_dict["examples"].append(exam_dict)
        catalogue.append(new_dict)
        save_intents(catalogue)
    save_intents(catalogue)


# Update the name of an intent
def change_intent_name(catalogue):
    print("\nUpdate the name of an intent..")
    code = code_input()
    intent_item = next(item for item in catalogue if item["ID"] == code)
    print(f"""\nCurrent intent name is "{intent_item["intent"]}" """)
    intent_item["intent"] = input("Please type the new name now: ")
    print(f"\nYou have successfully edited the intent name. The updated name now reads:\n{intent_item['intent']}")
    save_intents(catalogue)


# Update an existing intent example
def edit_intent(catalogue):
    print("\nUpdate the examples in an intent...")
    code = code_input()
    intent_item = next(item for item in catalogue if item["ID"] == code)
    print(f"""\nCurrent examples for the "{intent_item["intent"]}" intent:""")
    counter = 1
    for items in intent_item["examples"]:
        print(f"Intent example ({counter}) -> {items}")
        counter = counter + 1
    intent_example_selected = int(input("\nWhich intent example do you want to edit, example number: "))
    if intent_example_selected <= 0:  # if they pick 2x wrong numbers it breaks --- while true: can fix this, I don't know how yet.
        intent_example_selected = int(input("\nNo intent was found with that number, please specify number again: "))
        intent_example_selected = intent_example_selected - 1
        print(f"\nIntent selected: {intent_item['examples'][intent_example_selected]}")
        intent_item["examples"][intent_example_selected]['text'] = input("Please type the edited example now: ")
        print(
            f"\nYou have successfully edited the example. The updated example now reads:\n{intent_item['examples'][intent_example_selected]}")
    elif intent_example_selected > len(intent_item["examples"]):  # if they pick 2x wrong numbers it breaks
        intent_example_selected = int(input("\nNo intent was found with that number, please specify number again: "))
        intent_example_selected = intent_example_selected - 1
        print(f"\nIntent selected: {intent_item['examples'][intent_example_selected]}")
        intent_item["examples"][intent_example_selected]['text'] = input("Please type the edited example now: ")
        print(
            f"\nYou have successfully edited the example. The updated example now reads:\n{intent_item['examples'][intent_example_selected]}")
    else:
        intent_example_selected = intent_example_selected - 1
        print(f"\nIntent selected: {intent_item['examples'][intent_example_selected]}")
        intent_item["examples"][intent_example_selected]['text'] = input("Please type the edited example now: ")
        print(
                f"\nYou have successfully edited the example. The updated example now reads:\n{intent_item['examples'][intent_example_selected]}")
    save_intents(catalogue)


# Add an example to an intent
def add_example(catalogue):
    print("\nAdd an example to an intent..")
    code = code_input()
    intent_item = next(item for item in catalogue if item["ID"] == code)
    print(f"""\nCurrent selected intent is "{intent_item["intent"]}" """)
    print_check = input(
        "Do you want to see all examples for this intent(Y/N)? ")  # will also trigger if only 1 example AFTER deletion of ALL others - no issue here, just means 1 extra button for user to press.
    if print_check == "Y" or print_check == "y":
        print(f"\nCurrent examples for the '{intent_item['intent']}' intent:")
    print_counter = 1
    for item in intent_item["examples"]:
        print(f"Intent number ({print_counter}) -> {item}")
        print_counter = print_counter + 1
    add_count = int(input("\nHow many examples do you want to add? "))
    for i in range(add_count):
        exam = input(f"Example {i + 1}: ")
        exam_dict = {"text": exam}
        intent_item["examples"].append(exam_dict)
    print(f"""\nUpdated examples for the "{intent_item["intent"]}" intent:""")
    counter = 1
    for items in intent_item["examples"]:
        print(f"Intent number ({counter}) -> {items}")
        counter = counter + 1
    save_intents(catalogue)


# Remove an example from an intent
def remove_example(catalogue):
    print("\nRemove an example from an intent..")
    code = code_input()
    intent_item = next(item for item in catalogue if item["ID"] == code)
    print(f"""\nCurrent selected intent is "{intent_item["intent"]}" """)
    print_check = input("Do you want to see all examples for this intent(Y/N)?")
    if print_check == "Y" or print_check == "y":
        print(f"""\nCurrent examples for the "{intent_item["intent"]}" intent:""")
        counter = 1
        for items in intent_item["examples"]:
            print(f"Intent number ({counter}) -> {items}")
            counter = counter + 1
    intent_example_selected = int(input("\nWhich intent example do you want to remove? Example number: "))
    if intent_example_selected <= 0:
        intent_example_selected = int(input("\nNo example was found with that number, please specify number again: "))
        intent_example_selected = intent_example_selected - 1
        print(f"\nExample selected: {intent_item['examples'][intent_example_selected]}")
        del_check = input("Are you sure you want to delete this example(Y/N)?")
        if del_check == "Y" or del_check == "y":
            del intent_item["examples"][intent_example_selected]
    else:
        intent_example_selected = intent_example_selected - 1
        print(f"\nExample selected: {intent_item['examples'][intent_example_selected]}")
        del_check = input("Are you sure you want to delete this example(Y/N)?")
        if del_check == "Y" or del_check == "y":
            del intent_item["examples"][intent_example_selected]
    save_intents(catalogue)


# Save intents to new JSON
def save_prompt(catalogue):
    print("\nTo save your new file, please only use lowercase letters, numbers and spaces(or underscores).")
    save_changes = input(f"\nWhat should the name of the new file be?")
    with open(f"{save_changes}.json", "w") as f:
        json.dump(catalogue, f, indent=4)
    print("\nChanges were saved successfully!")


# Save intents continuously to JSON (as backup)
def save_intents(catalogue):
    with open("new_intents_test.json", "w") as f:
        json.dump(catalogue, f, indent=4)
    print("\nChanges were saved successfully!")
    # with open('data.json', 'w', encoding='utf-8') as f:
    # json.dump(data, f, ensure_ascii=False, indent=4)
    # there might be reason to use these later, if there are issues with encoding between the XML and the JSON - look here first


def code_input():
    code = input("Enter intent code: ")
    lc = re.compile("[a-z]+")
    low_g = lc.findall(code)
    if low_g == ["g"]:
        code = "G" + code[1]
    return code


# start main program
init_catalogue = initialise_catalogue()
print("\nWelcome to the intent catalogue")
print("-------------------------------\n")
while True:
    # Print out the menu:
    print("Please select an option :")
    print("1  List intents")
    print("2  View intent details")
    print("3  Create new intent")
    print("4  Update the name of an intent")
    print("5  Update an existing intent example")
    print("6  Add an example to an intent")
    print("7  Remove an example from an intent")
    print("S  Save all changes to a new file")
    print("W  Serialise for Export to Watson VA")
    print("X  Exit")

    # Get the user's choice:
    choice = input("> ")
    # Carry out task:
    if choice == '1':
        show_all_intents(init_catalogue)
    elif choice == '2':
        intent_detail(init_catalogue)
    elif choice == '3':
        create_intent(init_catalogue)
    elif choice == '4':
        change_intent_name(init_catalogue)
    elif choice == '5':
        edit_intent(init_catalogue)
    elif choice == '6':
        add_example(init_catalogue)
    elif choice == '7':
        remove_example(init_catalogue)
    elif choice == 'S' or choice == 's':
        save_prompt(init_catalogue)
    elif choice == 'X' or choice == 'x':
        print("Bye")
        break
    else:
        print("Invalid choice")
    print()
