import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import math as m
import sys
import tkinter as tk
import re

root = tk.Tk()

VOLTAGE = 0.0 # the initial Voltage the experiment starts with
WAVE_RES = 0.0 # wave resintance of the test setup
REFLECT_RES_0 = 0.0 # the resistence at the start of the measuring range
REFLECT_RES_l = 9*10e100 # the resistence at the end of the measuring range
LENGTH = 0.0 
C_PER_M = 0.0 
PERIODS = 0

volt_h = 0  # wave overshoot 0 to l
volt_r = 0 # wave overshoot l to 0
volt_0 = 0 # voltage at beginning of the measureing range
volt_l = 0 # voltage at the end of the measuring range

debugmode = false

def f(t):
    global volt_h
    global volt_r
    global volt_0
    global volt_l
    global result

    
    if t == 0:
        volt_h = VOLTAGE * WAVE_RES/(REFLECT_RES_0 + WAVE_RES)
        volt_0 = VOLTAGE * WAVE_RES/(REFLECT_RES_0 + WAVE_RES)
        result = VOLTAGE * WAVE_RES/(REFLECT_RES_0 + WAVE_RES)
        if debugmode:
            print("U0", result)
            print("UH", volt_h)
        return result
    if t % 2 == 0:
        volt_h = reflected_wave_overshoot(volt_r, REFLECT_RES_0, WAVE_RES)
        result = new_voltage(volt_0, volt_r, REFLECT_RES_0, WAVE_RES)
        volt_0 = result
        if debugmode:
            print("U0", result)
            print("UH", volt_h)
        return result
    else:
        volt_r = reflected_wave_overshoot(volt_h, REFLECT_RES_l, WAVE_RES)
        result = new_voltage(volt_l, volt_h, REFLECT_RES_l, WAVE_RES)
        volt_l = result
        if debugmode:
            print("Ul", result)
            print("UR", volt_r)
        return result

def simulate_func(func, x_start, x_end, ylim, xlabel, ylabel):
    fig, ax = plt.subplots()


    t = np.arange(x_end + 1.0)
    h = np.arange(x_end + 1.0)
    h0 = np.arange(x_end + 1.0)
    hl = np.arange(x_end + 1.0)
    
    for x in range(len(t)):
        h[x] = func(t[x])
    
    for x in range(len(t)):
        if x % 2 == 1:
            hl[x] = h[x]
            if(x > 0): h0[x] = h[x-1]
        else:
            h0[x] = h[x]
            if(x > 0): hl[x] = h[x-1]


    ax.set(xlim=[x_start, x_end], ylim=[0, ylim], xlabel=xlabel, ylabel=ylabel)

    ax.grid(True)
    plt.step(t, h0, where='post', label="V at l = 0")
    plt.step(t, hl, where='post', label="V at l = l")
    plt.legend()
    plt.show()
    
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    del t
    del h
    del h0
    del hl

# calculates the reflected wave overshoot or undershoot
def reflected_wave_overshoot(voltage, reflect_res, wave_res):
    reflection_fak = (reflect_res - wave_res) / (reflect_res + wave_res)
    return reflection_fak * voltage

# calculates the new voltage at the end with the upcoming wave overshoot
# and the resistence and Waveresistence
def new_voltage(old_volt, wave_diff, res, wave_res):
    reflection_fak = (res - wave_res) / (res + wave_res)
    return old_volt + wave_diff * (1+reflection_fak)

def reflection_time(wave_res, length, capacity_per_meter):
    return wave_res * length * capacity_per_meter * 10e-4


def get_user_input():
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)
    parameters = [
        ("Voltage", "V"),
        ("Wave Resistor", "Ω"),
        ("Reflection Resistor 1", "Ω"),
        ("Reflection Resistor 2", "Ω"),
        ("Length", "m"),
        ("Capacity per m", "pF/m"),
        ("Periods", ""),
    ]


    def validate(string):
        result = re.match(r"(\+|\-)?\d+(,\d+)?$", string)
        return result is not None

    vcmd = (root.register(validate), "%P")

    entries = {}
    for row, (label, unit) in enumerate(parameters):
        tk.Label(frame, text=f"{label}:").grid(
            row=row, column=0, sticky="e", padx=5, pady=5
        )
    
        entry = tk.Entry(frame, validate="key", validatecommand=vcmd)
        entry.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
    
        tk.Label(frame, text=unit).grid(
            row=row, column=2, sticky="w", padx=5, pady=5
        )
        entries[label] = entry
    
        def show_wave():
            for param, entry in entries.items():
                value = entry.get()
                global VOLTAGE, WAVE_RES, REFLECT_RES_0, REFLECT_RES_l, LENGTH, C_PER_M, PERIODS
                match param:
                    case "Voltage":
                        VOLTAGE = float(value)
                    case "Wave Resistor":
                        WAVE_RES = float(value)
                    case "Reflection Resistor 1":
                        REFLECT_RES_0 = float(value)
                    case "Reflection Resistor 2":
                        REFLECT_RES_l = float(value)
                    case "Length":
                        LENGTH = float(value)
                    case "Capacity per m":
                        C_PER_M = float(value)
                    case "Periods":
                        PERIODS = float(value)
                    case _:
                        print(Failed)

            print(VOLTAGE)
            print(WAVE_RES)
            print(REFLECT_RES_0)
            print(REFLECT_RES_l)
            print(LENGTH)
            print(C_PER_M)
            print(PERIODS)


            global volt_h
            global volt_r
            global volt_0
            global volt_l
            global result
            
            volt_h = 0 
            volt_r = 0
            volt_0 = 0
            volt_l = 0
            result = 0


            simulate_func(f, 0, PERIODS, 8.0, "T in " + str(reflection_time(WAVE_RES, LENGTH, C_PER_M)) + " ns", 'Spannung in V')

        tk.Button(frame, text="Submit", command=show_wave).grid(
            row=len(parameters), column=1, pady=10
        )
    
    root.mainloop()
get_user_input()
