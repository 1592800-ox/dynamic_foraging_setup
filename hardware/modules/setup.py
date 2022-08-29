import tkinter as tk
from hardware.modules import pump_ctrl

def setup(pump: pump_ctrl.Pump):
    modes = {'motor_training', 'training_1', 'training_2', 'data_collection'}
    code = 'None'

    mice = ['JGED01', 'JGED02']

    window = tk.Tk()
    window.title('session setup')
    mouse_code = tk.StringVar(master=window, value='None') 
    mode = tk.StringVar(master=window, value='None') 

    def _quit():
        pump.close_valve()
        window.quit()
        window.destroy()


    label = tk.Label(window, text='Select the mouse code')
    label.pack()
    dropdown = tk.OptionMenu(window, mouse_code, *mice)
    dropdown.pack()
    dropdown_mode = tk.OptionMenu(window, mode, *modes)
    dropdown_mode.pack()


    open_button = tk.Button(window, text='open_valve', command=pump.open_valve)
    open_button.pack()
    close_button = tk.Button(window, text='close_valve', command=pump.close_valve)
    close_button.pack()
    exit_button = tk.Button(window, text='confirm', command=_quit)
    exit_button.pack()

    window.mainloop()

    code = mouse_code.get()
    mode = mode.get()

    return code, mode
