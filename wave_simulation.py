import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import math as m
import sys

VOLTAGE = float(sys.argv[1]) # the initial Voltage the experiment starts with
WAVE_RES = float(sys.argv[2]) # wave resintance of the test setup
REFLECT_RES_0 = int(sys.argv[3]) # the resistence at the start of the measuring range
REFLECT_RES_l = 9*10e100 # the resistence at the end of the measuring range
LENGTH = float(sys.argv[4])
C_PER_M = float(sys.argv[5]) * m.pow(10, -9)

volt_h = 0  # wave overshoot 0 to l
volt_r = 0 # wave overshoot l to 0
volt_0 = 0 # voltage at beginning of the measureing range
volt_l = 0 # voltage at the end of the measuring range

#TODO eventuell lokal implementieren
def f(t):
    global volt_h
    global volt_r
    global volt_0
    global volt_l

    
    if t == 0:
        volt_h = VOLTAGE * WAVE_RES/(REFLECT_RES_0 + WAVE_RES)
        volt_0 = VOLTAGE * WAVE_RES/(REFLECT_RES_0 + WAVE_RES)
        result = VOLTAGE * WAVE_RES/(REFLECT_RES_0 + WAVE_RES)
        print("U0", result)
        print("UH", volt_h)
        return result
    if t % 2 == 0:
        volt_h = reflected_wave_overshoot(volt_r, REFLECT_RES_0, WAVE_RES)
        result = new_voltage(volt_0, volt_r, REFLECT_RES_0, WAVE_RES)
        volt_0 = result
        print("U0", result)
        print("UH", volt_h)
        return result
    else:
        volt_r = reflected_wave_overshoot(volt_h, REFLECT_RES_l, WAVE_RES)
        result = new_voltage(volt_l, volt_h, REFLECT_RES_l, WAVE_RES)
        volt_l = result
        print("Ul", result)
        print("UR", volt_r)
        return result

#TODO So umschreiben, dass die Rechtecke mit hoher x achsenauflösung
# richtig angezeigt werden
def simulate_func(func, x_start, x_end, ylim, xlabel, ylabel):
    fig, ax = plt.subplots()       # a figure with a single Axes


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


    #line = ax.plot(t[0], h[0])[0]
    ax.set(xlim=[x_start, x_end], ylim=[0, ylim], xlabel=xlabel, ylabel=ylabel)

    #def update(frame):
    #    line.set_xdata(t)
    #    line.set_ydata(h)

    #ani = animation.FuncAnimation(fig=fig, func=update, frames=200, interval=10)
    ax.grid(True)
    plt.step(t, h0, where='post', label="V at l = 0")
    plt.step(t, hl, where='post', label="V at l = l")
    plt.legend()
    plt.show()                           # Show the figure.

#TODO kontrollieren(eventuell fehler)
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
    return wave_res * length * capacity_per_meter



simulate_func(f, 0, 10, 8.0, "T in " + str(reflection_time(WAVE_RES, LENGTH, C_PER_M)), 'Spannung in V')
