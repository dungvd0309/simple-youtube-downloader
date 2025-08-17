def func():
    print("A function has been run")

menu_dict = {
    "1": ("Video with audio", func),
    "2": ("Video only", func),
    "3": ("Audio only", func),
    "4": ("Manual choice", func),
    "4": ("Thumbnail", func),
    "q": ("Quit", quit),
}

def run_menu():
    for key, (desc, f) in menu_dict.items():
        print(f"{key}. {desc}")
    choice = input("Choice: ")
    menu_dict.get(choice)[1]() # Run the chosen function
    menu_dict.keys()
run_menu()