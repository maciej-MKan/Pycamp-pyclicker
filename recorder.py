import json
from pynput.mouse import Listener as MouseListener
from time import sleep

class MouseRecorder:
    def __init__(self) -> None:
        self._moves = []
        self._listener = MouseListener(on_move= lambda x ,y : self._moves.append((x, y)))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._listener.stop()

    def record(self, run_time = 0):
        self._listener.start()
        sleep(run_time)
    
    def save(self, output_file = 'out.json'):
        with open(output_file, 'w') as file:
            json.dump(self._moves, file)

if __name__ == '__main__':
    with MouseRecorder() as recorder:
        recorder.record(15)
        recorder.save()