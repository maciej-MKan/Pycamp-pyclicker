#!/usr/bin/env python3.8

"""Module that records mouse and keyboard events"""

import json
from time import sleep
from itertools import cycle
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import KeyCode, Listener as KeyListener


class MouseRecorder:
    """The class that starts the hooking of mouse events"""
    def __init__(self, record_container : list) -> None:
        self._listener = MouseListener(
            on_move= self._on_move,
            on_click= self._on_click,
            on_scroll= self._on_scroll
        )
        self.events = record_container
        self.start_record()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._listener.stop()

    def _on_move(self, pos_x, pos_y):
        """records mouse movements"""
        self.events.append({'mouse': {'move': (pos_x, pos_y)}})

    def _on_click(self, *args):
        """records mouse buttons clicks"""
        *_, button, pressed = args
        self.events.append({'mouse': {'click': {button.name : pressed}}})

    def _on_scroll(self, *args):
        """ToDo : records mouse scrol events"""
        print(args)

    def start_record(self):
        """starts mouse listener"""
        self._listener.start()

    def __del__(self):
        """stops the keyboard listener when an instance of the class is destroyed"""
        self._listener.stop()


class KeyboardRecorder:
    """The class that starts the hooking of keyboard events"""
    def __init__(self, record_container : list, stop_flag) -> None:
        self._listener = KeyListener(
            on_press= self._on_press,
            on_release= self._on_release
        )
        self.events = record_container
        self.stop_flag = stop_flag
        self.start_record()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._listener.stop()

    def _on_press(self, pressed_key : KeyCode):
        """records keystrokes, if Esc is pressed call recording stop"""

        try:
            self.events.append({'keyboard': {'press': pressed_key.char}})
        except AttributeError:
            if str(pressed_key) == 'Key.esc':
                self.stop_flag()
            else:
                self.events.append({'keyboard': {'press': str(pressed_key)}})

    def _on_release(self, rel_key : KeyCode):
        """registers when a key is released"""
        try:
            self.events.append({'keyboard': {'release': rel_key.char}})
        except AttributeError:
            self.events.append({'keyboard': {'release': str(rel_key)}})

    def start_record(self):
        """starts keyboard listener"""
        self._listener.start()

    def __del__(self):
        """stops the keyboard listener when an instance of the class is destroyed"""
        self._listener.stop()

class MainRecorder:
    """The class linkinging and unifying the operation of recorders"""

    def __init__(self, stop_flag = None) -> None:
        """recorder initialization parameters

        Args:
            stop_flag (functjon, optional): Function that puts a flag to stop the recorder.
                                            Defaults to self._inner_stop_flag.

        Fields:
            self.events (list): list of the recorded steps
            self.stop_recording (bool): flag to stop the recorder
            self.recorders (list): list of recorders
            self.stop_flag (functjon): function that puts a flag to stop the recorder
        """
        self.events = []
        self.stop_recording = False
        self.recorders = []
        self.stop_flag = stop_flag
        if not stop_flag:
            self.stop_flag = self._inner_stop_flag

    def _init_recorders(self):
        """method includes unit recorders to the list of recorders"""
        self.recorders.append(MouseRecorder(self.events))
        self.recorders.append(KeyboardRecorder(self.events, self.stop_flag))

    def _inner_stop_flag(self):
        """default method to stop the recorder"""
        self.stop_recording = True

    def record(self, rec_time : float):
        """method to start recorders as context manager

        Args:
            rec_time (float): max recording time
        """
        self.events.clear()
        sleep(0.2)
        with MouseRecorder(self.events):
            with KeyboardRecorder(self.events, self.stop_flag):
                cur_time = 0
                for frame in cycle(r'-\|/-\|/'):
                    print('\r', frame, sep='', end='', flush=True)
                    sleep(0.2)
                    cur_time += 0.2
                    if cur_time >= rec_time or self.stop_recording:
                        self.stop_recording = False
                        break

    def start_record(self):
        """method start recorders"""

        self.events.clear()
        self._init_recorders()

    def stop_record(self):
        """method to stop the recorder, after using it,
        the recorder must be reinitialized before restarting"""
        self.recorders.clear()

    def save(self, output_file = 'out'):
        """method to save macro to file as json

        Args:
            output_file (str, optional): Name of file. Defaults to 'out'.
        """
        output_dict = {'property': None, 'steps': self.events}
        with open(f'{output_file}.json', 'w', encoding='utf-8') as file:
            json.dump(output_dict, file, indent=4)
        self.events.clear()

if __name__ == '__main__':
    main_recorder = MainRecorder()
    main_recorder.record(15)
    main_recorder.save()
