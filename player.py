import json
from pynput.mouse import Controller
from time import sleep

mouse = Controller()

with open('out.json', 'r') as file:
    moves = json.load(file)
    for single_move in moves:
        mouse.position = tuple(single_move)
        sleep(0.02)

