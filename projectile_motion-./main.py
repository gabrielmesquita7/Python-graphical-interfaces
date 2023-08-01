from tkinter import *
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

g = 9.81  # valor da gravidade na terra

listnumbers = [0.0000, 0.0000, 0.0000]
listnumbers2 = [00.000, 00.000]

root = Tk()
root.title('Lançamento Obliquo')
root.configure(bg='white')
root.geometry('650x700')

for i in range(10):
    if i < 10:
        Grid.columnconfigure(root, i, weight=1)
    Grid.rowconfigure(root, i, weight=1)

# Functions


def callback():
    global listnumbers
    time = int(listnumbers[0] * 1000 + (listnumbers[0]
               * 1000 / 2) + 1000)
    calcular.config(state=DISABLED)
    calcular.after(time, lambda: calcular.config(state=NORMAL))


def get_known_values():
    known = {}
    if vo.get() != '':
        if vo.get().isnumeric() == False and ("." in vo.get()) == False:
            messagebox.showerror("Erro", "Digite um valor válido")
        vo1 = float(vo.get())
        known.update({'vo': vo1})
    else:
        messagebox.showerror("Erro", "Digite o valor da velocidade")
    if a.get() != '':
        if a.get().isnumeric() == False and ("." in a.get()) == False:
            messagebox.showerror("Erro", "Digite um valor válido")
        a1 = float(a.get())
        known.update({'a': a1})
    else:
        messagebox.showerror("Erro", "Digite o valor do angulo")
    return known


def clear_values():
    vo.delete(0, END)
    a.delete(0, END)


def graphValues():
    global listnumbers2
    known = get_known_values()
    vo2 = known['vo']
    a2 = known['a'] * np.pi / 180
    listnumbers2[0] = vo2
    listnumbers2[1] = a2


def calc_t():
    global listnumbers
    known = get_known_values()
    vo2 = known['vo']
    a2 = known['a'] * np.pi / 180  # transforma graus em radianos
    t1 = 2 * vo2 * np.sin(a2) / g
    listnumbers[0] = t1
    result_time.configure(text=f'Tempo: {round(listnumbers[0], 4)} s')


def calc_alc():
    global listnumbers
    known = get_known_values()
    vo2 = known['vo']
    a2 = known['a'] * np.pi / 180
    alc1 = (vo2**2) * np.sin(2*a2) / g
    listnumbers[1] = alc1
    result_alc.configure(text=f'Alcance: {round(listnumbers[1], 4)} m')


def calc_am():
    global listnumbers
    known = get_known_values()
    vo2 = known['vo']
    a2 = known['a'] * np.pi / 180
    am = ((vo2**2) * (np.sin(a2)**2))/(2*g)
    listnumbers[2] = am
    result_am.configure(text=f'Altura maxima: {round(listnumbers[2], 4)} m')


# Tkinter visual elements
label1 = Label(root, text='Digite o valor das variaveis',
               font=("Arial", 14), bg='white')
label1.grid(row=0, column=0, columnspan=3, padx=0, pady=10, sticky='NESW')

vo_label = Label(root, text='Velocidade Inicial(m/s)', bg='white')
vo_label.grid(row=1, column=0, columnspan=1, padx=0, pady=5, sticky='NESW')
vo = Entry(root, borderwidth=5, justify=CENTER)
vo.focus_force()
vo.grid(row=1, column=1, columnspan=1, padx=0, pady=5, sticky='NESW')

a_label = Label(root, text='Angulo(graus)', bg='white')
a_label.grid(row=2, column=0, columnspan=1, padx=0, pady=5, sticky='NESW')
a = Entry(root, borderwidth=5, justify=CENTER, bg='white')
a.focus_force()
a.grid(row=2, column=1, columnspan=1, padx=0, pady=5, sticky='NESW')

clear_button = Button(root, text='Limpar',
                      command=clear_values, font='bold').grid(row=1, column=2, columnspan=1, padx=50, pady=10, sticky='NESW')
calcular = Button(root, text='Calcular ',
                  command=lambda: [calc_t(), calc_alc(), calc_am(), graphValues(), animação(), callback()], font='bold')
calcular.grid(row=2, column=2, columnspan=1, padx=50, pady=10, sticky='NESW')

empty_space = Label(root, bg='white').grid(
    row=3, column=0, columnspan=4, padx=0, pady=10, sticky='NESW')
result_time = Label(
    root, text=f'Tempo: {round(listnumbers[0], 4)} s', font=("Arial", 14), bg='white')
result_time.grid(row=4, column=0, columnspan=1,
                 padx=0, pady=20, sticky='NESW')
result_alc = Label(
    root, text=f'Alcance: {round(listnumbers[1], 4)} m', font=("Arial", 14), bg='white')
result_alc.grid(row=4, column=1, columnspan=1, padx=0, pady=20, sticky='NESW')
result_am = Label(
    root, text=f'Altura maxima: {round(listnumbers[2], 4)} m', font=("Arial", 14), bg='white')
result_am.grid(row=4, column=2, columnspan=1, padx=0, pady=20, sticky='NESW')

# Grafico

fig, ax = plt.subplots()
plt.grid(True)
# calculos
g = 9.81  # value of gravity
v = listnumbers2[0]
theta = listnumbers2[1]
t = 2 * v * np.sin(theta) / g
r_for_h = v*np.cos(theta)*(t/2)
h = ((v**2) * (np.sin(theta)**2))/(2*g)
r = (v**2) * np.sin(2*theta) / g


# estatisticas

plt.plot(r, 0, 'go')
plt.plot(r_for_h, h, 'ro')


t = np.arange(0, 0.1, 0.01)  # time of flight into an array
x = np.arange(0, 0.1, 0.01)
line, = ax.plot(x, v * np.sin(theta) * x - (0.5) *
                g * x**2)   # plot of x and y in time

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()

canvas.get_tk_widget().grid(row=5, column=0, columnspan=4, padx=10, pady=0)


# Projetil


plt.axhline(0, color='black')
plt.axvline(0, color='black')
plt.xlabel('Distance (x)')
plt.ylabel('Distance (y)')
plt.axis([0, 50.0, 0, 8.0])
ax.set_autoscale_on(False)


def animação():
    global listnumbers
    ax.clear()
    # calculos
    g = 9.81  # value of gravity
    v = listnumbers2[0]
    theta = listnumbers2[1]
    t = 2 * v * np.sin(theta) / g
    r_for_h = v*np.cos(theta)*(t/2)
    h = ((v**2) * (np.sin(theta)**2))/(2*g)
    r = (v**2) * np.sin(2*theta) / g
    if theta == 1.5707963267948966:
        r = 0.0
        r_for_h = 0.0

    int_t = int(t*100)
    plt.plot(r, 0, 'go', linewidth=10, markersize=10)
    plt.plot(r_for_h, h, 'ro')

    t = np.arange(0, 0.1, 0.01)
    x = np.arange(0, 0.1, 0.01)
    line, = ax.plot(x, v * np.sin(theta) * x - (0.5) *
                    g * x**2)
    # Projetil

    def animate(i):
        plt.grid(True)
        line.set_linestyle("-")
        line.set_linewidth(3.5)
        line.set_xdata(v * np.cos(theta) * (t + i / 100.0))
        line.set_ydata(v * np.sin(theta) * (x + i / 100.0) -
                       (0.5) * g * (x + i / 100.0)**2)
        return line,

    plt.axhline(0, color='black')
    plt.axvline(0, color='black')
    plt.xlabel('Distancia(x) m')
    plt.ylabel('Distancia(y) m')

    if h <= 1.00:
        plt.axis([0, r+r/5, 0, 1])
    if h > 1.00:
        plt.axis([0, r+r/5, 0, 50])
    if h > 50.00:
        plt.axis([0, r+r/5, 0, 100])

    ax.set_autoscale_on(False)

    ani = animation.FuncAnimation(
        fig, animate, frames=int_t+2, interval=10, blit=True, repeat=False)
    canvas.draw()


root.mainloop()
