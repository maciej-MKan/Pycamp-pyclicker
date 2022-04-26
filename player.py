import json
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyController
from time import sleep

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
        specjal = key_to_press.split('.')
        if len(specjal) > 1:
            key_to_press = getattr(Key, specjal[1])
        self.controler.press(key_to_press)

    def release(self, key_to_rel : str):
        specjal = key_to_rel.split('.')
        if len(specjal) > 1:
            key_to_rel = getattr(Key, specjal[1])
        self.controler.release(key_to_rel)

class Player:
    def __init__(self) -> None:
        self.mouse = Mouse()
        self.keyboard = Keyboard()

    def load_commands(self):
        with open('out.json', 'r') as file:
            commands = json.load(file)
            for command in commands:
                device_name, *_ = command.keys()
                device = getattr(self, device_name)
                event = command[device_name]
                event_type, *_ = event.keys()
                event_args = event[event_type]
                #print(device, ' ', event, ' ', event_type, ' ', event_args)
                getattr(device, event_type)(event_args)
                sleep(0.05)




if __name__ == '__main__':
    player = Player()
    player.load_commands()

