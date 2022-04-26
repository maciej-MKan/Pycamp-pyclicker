import json
from time import sleep
from itertools import cycle
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import KeyCode, Listener as KeyListener

class StopRecording(Exception):
    """exc to stop rec"""

class MouseRecorder:
    def __init__(self, record_container : list) -> None:
        self._listener = MouseListener(
            on_move= self._on_move,
            on_click= self._on_click,
            on_scroll= self._on_scroll
        )
        self._listener.start()
        self.events = record_container

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._listener.stop()

    def _on_move(self, pos_x, pos_y):
        self.events.append({'mouse': {'move': (pos_x, pos_y)}})

    def _on_click(self, *args):
        *_, button, pressed = args
        self.events.append({'mouse': {'click': {button.name : pressed}}})

    def _on_scroll(self, *args):
        print(args)

class KeyboardRecorder:
    def __init__(self, record_container : list) -> None:
        self._listener = KeyListener(
            on_press= self._on_press,
            on_release= self._on_release
        )
        self._listener.start()
        self.events = record_container

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._listener.stop()

    def _on_press(self, pressed_key : KeyCode):
        try:
            self.events.append({'keyboard': {'press': pressed_key.char}})
        except AttributeError as exc:
            if str(pressed_key) == 'Key.esc':
                self._listener.stop()
                raise StopRecording from exc

            self.events.append({'keyboard': {'press': str(pressed_key)}})

    def _on_release(self, rel_key : KeyCode):
        try:
            self.events.append({'keyboard': {'release': rel_key.char}})
        except AttributeError:
            self.events.append({'keyboard': {'release': str(rel_key)}})

class MainRecorder:

    def __init__(self) -> None:
        self._events = []

    def record(self, rec_time):
        with MouseRecorder(self._events):
            with KeyboardRecorder(self._events):
                cur_time = 0
                for frame in cycle(r'-\|/-\|/'):
                    print('\r', frame, sep='', end='', flush=True)
                    sleep(0.2)
                    cur_time += 0.2
                    if cur_time >= rec_time:
                        break

        #print(self._events)


    def save(self, output_file = 'out'):
        with open(f'{output_file}.json', 'w', encoding='utf-8') as file:
            json.dump(self._events, file, indent=4)
        self._events.clear()

if __name__ == '__main__':
    main_recorder = MainRecorder()
    main_recorder.record(15)
    main_recorder.save()
