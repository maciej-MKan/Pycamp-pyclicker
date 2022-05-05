#!/usr/bin/env python3.8

"""The main module of the graphic version of the program"""

import tkinter as tk
import json

import recorder
import player

class Gui(tk.Frame):
    """Main class inheriting from tkinter.Frame. Creates, sets and programs widgets"""
    def __init__(self, master = None) -> None:
        super().__init__(master)
        self.master = master
        self.pack()
        self.recorder = recorder.MainRecorder(stop_flag=self.stop_currnt_record)
        self.player = player.Player()
        self.window_recorder = None
        self.wr_label = None
        self.create_widgets()

    def create_widgets(self):
        """Creates, sets and programs widgets of root window"""

        self.bt_record = tk.Button(self)
        self.bt_record['text'] = 'Record new'
        self.bt_record['command'] = self.start_new_record

        self.bt_replay = tk.Button(self)
        self.bt_replay['text'] = 'Replay macro'
        self.bt_replay['command'] = lambda : self.repaly(0)

        self.bt_load = tk.Button(self)
        self.bt_load['text'] = 'Load macro'
        self.bt_load['command'] = self.load

        self.bt_save = tk.Button(self)
        self.bt_save['text'] = 'Save'
        self.bt_save['command'] = self.save

        self.entry_macro = tk.Text(self, width=32, height= 25, padx=2, pady=2)
        self.scroll_macro = tk.Scrollbar(self, command=self.entry_macro.yview)
        self.entry_macro['yscrollcommand'] = self.scroll_macro.set

        self.bt_record.grid(column= 1, row= 0, columnspan= 3, pady= 10)
        self.bt_replay.grid(column= 6, row= 1, columnspan= 3, pady= 10)
        self.bt_load.grid(column= 1, row= 1, columnspan= 3, pady= 10)
        self.bt_save.grid(column= 6, row= 0, columnspan= 3, pady= 10)
        self.entry_macro.grid(column= 0, row= 2, columnspan= 9,  sticky="nsew")
        self.scroll_macro.grid(column= 9, row= 2, sticky='nsew')

    def create_recorder_widget(self):
        """Creates, sets and programs widgets of recorder sub-window"""
        self.window_recorder = tk.Toplevel(self)
        self.window_recorder.title('PyClicker - recording ...')
        self.window_recorder.resizable(False,False)
        self.window_recorder.transient(self)
        self.wr_label = tk.Label(self.window_recorder)
        self.wr_label['text'] = 'Now recording...\nTo stop press Esc'
        self.window_recorder.protocol("WM_DELETE_WINDOW", self.stop_currnt_record)
        #self.master.iconify()
        self.wr_label.pack()

    def start_new_record(self):
        """call creates a recorder window and starts macro recording"""
        self.entry_macro.delete('1.0', 'end')
        self.entry_macro.insert('end', 'To stop recording press Esc key')
        self.create_recorder_widget()
        self.recorder.start_record()

    def stop_currnt_record(self):
        """stops macro recording, sets macro content to widget, destroys recorder window"""
        self.recorder.stop_record()
        self.window_recorder.destroy()
        self.entry_macro.delete('1.0', 'end')
        self.entry_macro.insert('end', json.dumps(self.recorder.events, indent=2))
        #self.master.deiconify()

    def repaly(self, step : int):
        """runs macro from widget

        Args:
            step (int): the number of steps in the macro to play back
        """
        try:
            comand = json.loads(self.entry_macro.get('1.0','end'))[step]
            self.player.play_commands((comand,), sleep_time = 0)
            step += 1
            self.after(20, self.repaly, step)
        except IndexError:
            return

    def load(self):
        """loads macro from file and put them to widget"""
        self.entry_macro.insert('end', json.dumps(self.player.load_macro()['steps'], indent=2))

    def save(self):
        """safes macro from widget to file"""
        self.recorder.events = json.loads(self.entry_macro.get('1.0','end'))
        self.recorder.save()

def main():
    """Main method. Sets root window and start mainloop"""
    root = tk.Tk()
    root.geometry('300x500')
    root.title('PyClicker')
    app = Gui(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()
