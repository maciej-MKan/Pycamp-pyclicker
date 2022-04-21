from shutil import move
import pickle
from pynput.mouse import Controller
from time import sleep

mouse = Controller()

with open('out.txt', 'rb') as file:
    moves = pickle.load(file)
    for single_move in moves:
        mouse.position = single_move
        sleep(0.02)

