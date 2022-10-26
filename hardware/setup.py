import tkinter as tk
from hardware import pump_ctrl

def setup(pump: pump_ctrl.Pump, mice):
    padx = 50
    pady = 10
    code = 'None'

    window = tk.Tk()
    window.title('session setup')
    mouse_code = tk.StringVar(master=window, value='None') 

    def _quit():
        pump.close_valve()
        window.quit()
        window.destroy()


    label = tk.Label(window, text='Select the mouse code')
    label.pack(padx=padx, pady=pady)
    dropdown = tk.OptionMenu(window, mouse_code, *mice)
    dropdown.pack(padx=padx, pady=pady)
    label_mode = tk.Label(window, text='Select the training mode')
    label_mode.pack(padx=padx, pady=pady)

    label_pump = tk.Label(window, text='valve control')
    label_pump.pack(padx=padx, pady=pady)
    open_button = tk.Button(window, text='open_valve', command=pump.open_valve)
    open_button.pack(padx=padx, pady=pady)
    close_button = tk.Button(window, text='close_valve', command=pump.close_valve)
    close_button.pack(padx=padx, pady=pady)
    exit_button = tk.Button(window, text='confirm', command=_quit)
    exit_button.pack(padx=padx, pady=pady)

    window.mainloop()

    code = mouse_code.get()

    return code
