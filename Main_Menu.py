print("\nWelcome to the Asset's Main Menu")
print("-------------------------------\n")
while True:
    # Print out the menu:
    print("Please select an option :")
    print("1  Skill Extraction")
    print("2  Intent Catalogue")
    print("3  Entity Catalogue")
    print("4  XML Parsing and VA Creation")
    print("5  Catalogue and VA Compiler")
    print("X  Exit")

    # Get the user's choice:
    choice = input("> ")
    # Carry out task:
    if choice == '1':
        exec(open("Skill_Extraction.py").read())
    elif choice == '2':
        exec(open("Intent_Catalogue_WP.py").read())
    elif choice == '3':
        exec(open("Entity_Catalogue_WP.py").read())
    elif choice == '4':
        exec(open("MainScript_Deployment_WP_SLOTS_RESPONSE.py").read())
    elif choice == '5':
        exec(open("CompilerScript.py").read())
    elif choice == 'X' or choice == 'x':
        print("Bye")
        break
    else:
        print("Invalid choice")
    print()

