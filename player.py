import json
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyController
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

class Player:
    def __init__(self) -> None:
        self.mouse = Mouse()

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
                sleep(0.02)




if __name__ == '__main__':
    player = Player()
    player.load_commands()

