import tkinter as tk
from hardware.modules import pump_ctrl

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

    def _quit():
        window.quit()
        window.destroy()

    def _motor_cb():
        print(motor_cb_var.get())
    
    def _train_cb():
        print(train_cb_var.get())

    label = tk.Label(window, text='Select the mouse code')
    dropdown = tk.OptionMenu(window, mouse_code, *mice)


    motor_cb_var = tk.BooleanVar()
    train_cb_var = tk.BooleanVar()

    motor_cb_var.set(False)
    train_cb_var.set(False)

    motor_cb = tk.Checkbutton(window, text='Motor Training',  variable=motor_cb_var, command=_motor_cb)
    
    train_cb = tk.Checkbutton(window, text="Training (No need to check this if 'Motor Training' is checked)", variable=train_cb_var, onvalue=True, offvalue=False, command=_train_cb)

    open_button = tk.Button(window, text='open_valve', command=pump.open_valve)

    close_button = tk.Button(window, text='close_valve', command=pump.close_valve)

    exit_button = tk.Button(window, text='confirm', command=_quit)

    label.grid(column=0, row=0)
    dropdown.grid(column=1, row=0)
    motor_cb.grid(column=0, row=2)
    train_cb.grid(column=0, row=4)
    open_button.grid(column=0, row=6)
    close_button.grid(column=0, row=8)
    exit_button.grid(column=1, row=10)

    print('entered mainloop')
    window.mainloop()
    print('exited mainloop')

    code = mouse_code.get()
    motor_training = motor_cb_var.get()
    training = train_cb_var.get()

    print(code)
    print(training)

    return code, motor_training, training
