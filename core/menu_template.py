import os
import msvcrt


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def press_to_continue():
    print("Press any key to continue...", end="", flush=True)
    msvcrt.getch()


class AbstractMenu:
    
    def __init__(self, title: str):
        self.title: str = title
        # self.clear_console_on_execute = clear_console_on_execute

    @staticmethod
    def get_user_input():
        return input(" >> ")

    def display_menu(self):
        pass
    
    def execute_menu(self):
        if self.clear_console_on_execute:
            clear_console


class OptionMenu(AbstractMenu):

    def __init__(self, title: str):
        super().__init__(title)
        self.items: list[MenuItem] = [] 
        self.initialize_item_list()

    def initialize_item_list(self):
        """Add menu items with method add_menu_item."""
        pass

    def add_menu_item(self, item: 'MenuItem'):
        """Add a menu item to item list."""
        self.items.append(item)

    def display_menu(self):
        print(self.title)
        for item in self.items:
            item.show()

    def execute_menu(self):
        repeat = True
        while repeat:
            clear_console()
            self.display_menu()

            # Get user item id
            choice = self.get_user_input()

            # Find item and run item action
            for item in self.items:
                if choice == item.id:
                    item.run()
                    # Stop the menu if the item is exit option
                    if item.isExitOption:
                        repeat = False
                    break
        
class MenuItem:
    
    def __init__(
            self, 
            id: int | str, 
            desc: str, 
            action: callable = None, 
            menu: AbstractMenu = None, 
            isExitOption: bool = False
    ):
        self.id: str = str(id)
        self.desc: str = desc
        self.action: callable = action
        self.menu: OptionMenu = menu
        self.isExitOption: bool = isExitOption
    
    def show(self):
        print(f"[{self.id}] {self.desc}")

    def run(self):
        if self.action != None:
            self.action()
        if self.menu != None:
            self.menu.execute_menu()


class TextPromptMenu(AbstractMenu):

    def __init__(self, title: str):
        super().__init__(title)

    def display_menu(self):
        print(self.title)

    def execute_menu(self) -> str:
        clear_console()
        self.display_menu()
        return self.get_user_input()

        
class ResultMenu(AbstractMenu):
    def display_menu(self):
        print(self.title)

    @staticmethod
    def get_user_input():
        print("Press any key to continue...", end="", flush=True)
        msvcrt.getch()

    def execute_menu(self):
        # clear_console()
        self.display_menu()
        self.get_user_input()
