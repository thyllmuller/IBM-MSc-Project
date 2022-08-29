import io
import json
import os

path = os.getcwd()
file = "compiled_watson.json"
filepath = path + "\\" + file
print("\nInitialising system files.")
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

#name = input("What is the name of this skill?")
name = "Password Reset"

#description = input("Provide a brief description for this skill")
description = "Basic Password Reset Request"

final_details = {"learning_opt_out": False,
                 "name": name,
                 "language": "en",
                 "description": description}

final_json = {"intents": [json_intents], "entities": [json_entities], "metadata": json_meta, "dialogue": [json_dia],
              "counterexamples": [], "system_settings": json_settings}

for item in final_details:
    final_json[item] = final_details[item]
print(final_json)


with open("compiled_watson.json", "w") as f:
    json.dump(final_json, f, indent=4)
print("\nChanges were saved successfully!")



'''
newoverall_obj = {"intents": [], "entities": [], "metadata": {}, "dialogue": [], "counterexamples": [], "system_settings": {}}
for idx in json_entities:
    for entities2 in object:
        entitiesx = []
        entitiesx = append(entities)
    newoverall_obj["entities"] = entitiesx
    json_entities.append()

for idx in json_entities:
    for value in idx['values']:
        print(value['synonyms'])

'''

# print(json_entities[0]['values'][0])

# syn = []

# for idx in json_entities:
#    for value in idx['values']:
#        syn.append(value['synonyms'])

# print(syn)


'''
for idx in json_entities:
    for value in idx['values']:
        # do what you need with values
        print(value['value'])
        for syn in value['synonyms']:
            # do what you need with syns
            print(syn)
'''
