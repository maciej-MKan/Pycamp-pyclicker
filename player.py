#!/usr/bin/env python3.8

"""Module that replay mouse and keyboard events"""

import json
from time import sleep
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyController

class Mouse:
    """class to support mouse events"""
    def __init__(self) -> None:
        self.controler = MouseController()

    def move(self, args : tuple):
        """method that moves the mouse pointer to a new position

        Args:
            args (tuple): new position (x, y) in pixels

        Raises:
            AttributeError: exception when position is wrong
        """
        if len(args) == 2:
            pos_x, pos_y = args
            self.controler.position = (pos_x, pos_y)
        else:
            raise AttributeError(f'No 2 args {args}')

    def click(self, args : dict):
        """method that support mouse buttons

        Args:
            args (dict): button name, button action (true / false) pressed
        """
        button_name, *_ = args.keys()
        button = getattr(Button, button_name)
        pressed = args[button_name]
        if pressed:
            self.controler.press(button)
        else:
            self.controler.release(button)

class Keyboard:
    """class to support keyboard events"""
    def __init__(self) -> None:
        self.controler = KeyController()

    def press(self, key_to_press : str):
        """method that presses key

        Args:
            key_to_press (str): name of key
        """
        specjal = None
        if len(key_to_press) > 2:
            specjal = key_to_press.split('.')[1]
        if specjal:
            key_to_press = getattr(Key, specjal)
        self.controler.press(key_to_press)
        sleep(0.08)

    def release(self, key_to_rel : str):
        """method that releases key

        Args:
            key_to_rel (str): name of key
        """
        specjal = None
        if len(key_to_rel) > 2:
            specjal = key_to_rel.split('.')[1]
        if specjal:
            key_to_rel = getattr(Key, specjal)
        self.controler.release(key_to_rel)
        sleep(0.08)

class Player:
    """class that reads a macro and raises events from it"""
    def __init__(self) -> None:
        self.mouse = Mouse()
        self.keyboard = Keyboard()
        self.macro = None

    def load_macro(self, file_name = 'out'):
        """method that load macro from file

        Args:
            file_name (str, optional): File name. Defaults to 'out'.

        Returns:
            dict: macro
        """
        try:
            with open(f'{file_name}.json', 'r', encoding='utf-8') as file:
                self.macro = json.load(file)
        except FileNotFoundError:
            return {'steps': 'No macros to load'}
        return self.macro

    def play_commands(self, commands : tuple = None, sleep_time : float = 0.05):
        """method that execute steps from macro

        Args:
            commands (tuple, optional): Steps. Defaults to self.macro.
            sleep_time (float, optional): Pause between steps. Defaults to 0.05.
        """
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
