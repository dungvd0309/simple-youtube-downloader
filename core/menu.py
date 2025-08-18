import os
from typing import LiteralString

PROGRAM_TITLE = "Simple YouTube Downloader"

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def clear_console_before(func):
    def wrapper(*args, **kwargs):
        clear_console()
        return func(*args, **kwargs)
    return wrapper

def print_title_before(func):
    def wrapper(*args, **kwargs):
        print(PROGRAM_TITLE)
        print()
        return func(*args, **kwargs)
    return wrapper

@clear_console_before
def func():
    print("A function has been run")

# CONFIG
# choice : (desc, func)
download_options = {
    "title": "Download options",
    "1": ("Video with audio", func),
    "2": ("Video only", func),
    "3": ("Audio only", func),
    "4": ("Manual choice", func),
    "4": ("Thumbnail", func),
    "b": ("Back", func),
    "q": ("Quit", quit)
}

@clear_console_before
@print_title_before
def print_menu(menu_dict: dict):
    for key, (desc, f) in menu_dict.items():
        print(f" [{key}] {desc}")

@clear_console_before
@print_title_before 
def input_url():
    url = input("URL: ")
    return url

def run_menu(menu_dict: dict):
    while True:
        print_menu(download_options)
        choice = input(" >> ")
        action = download_options.get(choice)
        if action:
            action[1]() # Run the chosen function
        else: 
            input("Invalid choice. Press any key...")


# class MenuTemplate():

#     def __init__(self, options: dict):
#         self.options = options
    
#     @clear_console_before
#     @print_title_before
#     def print_menu(self):
#         print(self.options.get("title"))
        
#         for key, value in self.options.items():
#             if key != "title":
#                 desc = value[0]
#                 print(f" [{key}] {desc}")
    
#     def get_action(self):
#         self.print_menu()
#         choice = input(" >> ")
#         action = self.options.get(choice)
#         if action:
#             action[1]() # Run the chosen function
#         else: 
#             input("Invalid choice. Press any key...")

class MenuTemplate:
    pass

# class MenuItem:
#     def __init__(self, id: 'str', desc: 'str', action: callable = None, menu: MenuTemplate = None):
#         self.id = id
#         self.desc = desc
#         self.action = action
#         self.menu = menu
    
#     def show(self):
#         print(f"[{self.id}] {self.desc}")

#     def run(self):
#         pass
class MenuTemplate:

    def __init__(self, options: dict):
        self.options = options
    
    @clear_console_before
    @print_title_before
    def print_menu(self):
        print(self.options.get("title"))
        
        for key, value in self.options.items():
            if key != "title":
                desc = value[0]
                print(f" [{key}] {desc}")
    
    def get_action(self):
        self.print_menu()
        choice = input(" >> ")
        action = self.options.get(choice)
        if action:
            action[1]() # Run the chosen function
        else: 
            input("Invalid choice. Press any key...")

class UrlMenu(MenuTemplate):
    pass
class DownloadMenu(MenuTemplate):
    pass

class MenuHandler():
    
    def __init__(self):
        self.url_menu
        self.download_menu


if __name__ == "__main__": 
    # input_url()   
    # run_menu(download_options)

    download_menu = MenuTemplate(download_options)
    download_menu.execute_menu()