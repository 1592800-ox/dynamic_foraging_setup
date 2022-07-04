import tkinter as tk
from modules import pump_ctrl

def setup(pump: pump_ctrl.Pump):
    training = False
    motor_training = False
    code = 'None'

    paddings = {'padx': 5, 'pady': 5} 
    mice = ['JGED01', 'JGED02']

    window = tk.Tk()
    window.title('session setup')
    window.geometry('800x200')
    mouse_code = tk.StringVar(master=window, value='None') 

    label = tk.Label(window, text='Select the mouse code')
    label.grid(column=0, row=0)

    dropdown = tk.OptionMenu(window, mouse_code, *mice)
    dropdown.grid(column=1, row=0)

    motor_cb_var = tk.BooleanVar()
    motor_cb = tk.Checkbutton(window, text='Motor Training', onvalue=True, offvalue=False, variable=motor_cb_var)
    motor_cb.grid(column=0, row=2)

    train_cb_var = tk.BooleanVar()
    train_cb = tk.Checkbutton(window, text="Training (No need to check this if 'Motor Training' is checked)", onvalue=True, offvalue=False, variable=train_cb_var)
    train_cb.grid(column=0, row=4)

    open_button = tk.Button(window, text='open_valve', command=pump.open_valve)
    open_button.grid(column=0, row=6)

    close_button = tk.Button(window, text='close_valve', command=pump.close_valve)
    close_button.grid(column=0, row=8)

    exit_button = tk.Button(window, text='confirm', command=window.destroy)
    exit_button.grid(column=1, row=10)

    window.mainloop()

    code = mouse_code.get()
    motor_training = motor_cb_var.get()
    training = train_cb_var.get()

    return code, motor_training, training