import json
from pynput.mouse import Listener as MouseListener
from time import sleep

class MouseRecorder:
    def __init__(self) -> None:
        self._events = []
        self._listener = MouseListener(
            on_move= self._on_move,
            on_click= self._on_click,
            on_scroll= self._on_scroll
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._listener.stop()

    def _on_move(self, pos_x, pos_y):
        self._events.append({'mouse': {'move': (pos_x, pos_y)}})

    def _on_click(self, *args):
        *_, button, pressed = args
        self._events.append({'mouse': {'click': {button.name : pressed}}})

    def _on_scroll(self, *args):
        print(args)

    def record(self, run_time = 0):
        self._listener.start()
        sleep(run_time)

    def save(self, output_file = 'out.json'):
        with open(output_file, 'w') as file:
            json.dump(self._events, file, indent=4)

if __name__ == '__main__':
    with MouseRecorder() as recorder:
        recorder.record(15)
        recorder.save()