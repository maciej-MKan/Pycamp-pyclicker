import json
from pynput.mouse import Controller, Button
from time import sleep

class Player:
    def __init__(self) -> None:
        self.mouse = Controller()

    def load_commands(self):
        with open('out.json', 'r') as file:
            commands = json.load(file)
            for command in commands:
                key, *_ = command.keys()
                getattr(self, key)(command[key])
                sleep(0.02)

    def move(self, args):
        if len(args) == 2:
            pos_x, pos_y = args
            self.mouse.position = (pos_x, pos_y)
        else:
            raise AttributeError(f'No 2 args {args}')

    def click(self, args : dict):
        button_name, *_ = args.keys()
        button = getattr(Button, button_name)
        pressed = args[button_name]
        if pressed:
            self.mouse.press(button)
        else:
            self.mouse.release(button)


if __name__ == '__main__':
    player = Player()
    player.load_commands()

