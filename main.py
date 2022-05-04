#!/usr/bin/env python3.8

"""The main module console version of the program"""

import recorder
import player

def main():
    """Main module. Shows the user interface and runs the appropriate commands"""

    my_recorder = recorder.MainRecorder()
    my_player = player.Player()
    choice =''
    while choice != '3':
        choice = input('1 - record macro  2 - playback macro  3 - exit \n')
        if choice == '1':
            try:
                # ToDo - user selectable recording time
                my_recorder.record(20)
            except recorder.StopRecording:
                pass
            my_recorder.save(input('enter macro name : '))
        if choice == '2':
            my_player.load_macro(input('enter macro name : '))
            my_player.play_commands()

if __name__ == '__main__':
    main()
