import recorder
import player

def main():
    my_recorder = recorder.MainRecorder()
    my_player = player.Player()
    choice =''
    while choice != '3':
        choice = input('1 - record macro  2 - playback macro  3 - exit \n')
        if choice == '1':
            try:
                my_recorder.record(20)
            except recorder.StopRecording:
                pass
            my_recorder.save(input('enter macro name : '))
        if choice == '2':
            my_player.load_commands(input('enter macro name : '))

if __name__ == '__main__':
    main()
