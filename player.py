import json
from time import sleep
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyController

class Mouse:
    def __init__(self) -> None:
        self.controler = MouseController()

    def move(self, args):
        if len(args) == 2:
            pos_x, pos_y = args
            self.controler.position = (pos_x, pos_y)
        else:
            raise AttributeError(f'No 2 args {args}')

    def click(self, args : dict):
        button_name, *_ = args.keys()
        button = getattr(Button, button_name)
        pressed = args[button_name]
        if pressed:
            self.controler.press(button)
        else:
            self.controler.release(button)

class Keyboard:
    def __init__(self) -> None:
        self.controler = KeyController()

    def press(self, key_to_press : str):
        specjal = None
        if len(key_to_press) > 2:
            specjal = key_to_press.split('.')[1]
        if specjal:
            key_to_press = getattr(Key, specjal)
        self.controler.press(key_to_press)
        sleep(0.08)

    def release(self, key_to_rel : str):
        specjal = None
        if len(key_to_rel) > 2:
            specjal = key_to_rel.split('.')[1]
        if specjal:
            key_to_rel = getattr(Key, specjal)
        self.controler.release(key_to_rel)
        sleep(0.08)

class Player:
    def __init__(self) -> None:
        self.mouse = Mouse()
        self.keyboard = Keyboard()
        self.macro = None

    def load_macro(self, file_name = 'out'):
        try:
            with open(f'{file_name}.json', 'r', encoding='utf-8') as file:
                self.macro = json.load(file)
        except FileNotFoundError:
            return {'steps': 'No macros to load'}
        return self.macro

    def play_commands(self, commands : tuple = None, sleep_time : float = 0.05):
            if not commands:
                commands = self.macro['steps']
            for command in commands:
                device_name, *_ = command.keys()
                device = getattr(self, device_name)
                event = command[device_name]
                event_type, *_ = event.keys()
                event_args = event[event_type]
                getattr(device, event_type)(event_args)
                sleep(sleep_time)

if __name__ == '__main__':
    player = Player()
    player.load_macro()
    player.play_commands()
