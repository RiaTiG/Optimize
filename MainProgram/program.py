

import random
from random import uniform
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.pylab import uniform
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from scipy.optimize import minimize
import time

# Функция Экли
def ackley_function(x, y):
    return -20 * np.exp(-0.2 * np.sqrt(0.5 * ( x**2 + y** 2))) - np.exp(
        0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y))) + np.exp(1) + 20

# Градиент функции Экли
def gradient_ackley(x, y):
    part1 = 0.04 * x * np.exp(-0.2 * np.sqrt(0.5 * (x ** 2 + y ** 2))) / np.sqrt(0.5 * (x ** 2 + y ** 2))
    part2 = 0.04 * y * np.exp(-0.2 * np.sqrt(0.5 * (x ** 2 + y ** 2))) / np.sqrt(0.5 * (x ** 2 + y ** 2))
    part3 = 2 * np.pi * np.exp(0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y))) * np.sin(2 * np.pi * x)
    part4 = 2 * np.pi * np.exp(0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y))) * np.sin(2 * np.pi * y)
    dx = part1 - part3
    dy = part2 - part4
    return dx, dy

# Функция Матьяса
def matyas_function(x, y):
    return 0.26 * (x ** 2 + y ** 2) - 0.48 * x * y

# Градиент функции Матьяса
def gradient_matyas(x, y):
    dx = 0.52 * x - 0.48 * y
    dy = 0.52 * y - 0.48 * x
    return dx, dy

#Функция для 2 ЛР
def lr2Function(x1,x2):
    return 2 * x1 * x1 + 3 * x2 * x2 + 4 * x1 * x2 - 6 * x1 - 3 * x2

# Функция Букина N6
def bukin_function(x, y):
    return 100 * np.sqrt(np.abs(y - 0.01 * x ** 2)) + 0.01 * np.abs(x + 10)

def rosenbrock(x, y):
    return (1 - x)**2 + 100 * (y - x**2)**2

# Градиент функции Букина N6
def gradient_bukin(x, y):
    dx = 0.01 * (20 - 2 * x) / (2 * np.sqrt(np.abs(y - 0.01 * x ** 2))) + np.sign(x + 10)
    dy = np.float128(50) * (y - 0.01 * x ** 2) / np.sqrt(np.abs(y - 0.01 * x ** 2))
    return dx, dy

# Создание GUI окна
root = tk.Tk()
root.title("Оптимизация")

# Создание трехмерного графика
fig = plt.figure(figsize=(8, 6))
ax = plt.axes(projection='3d')

clons_var=tk.IntVar(value=20)
best_imun_var=tk.IntVar(value=10)
# Вставка графика в GUI окно
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=0, rowspan=14)

# Выбор функции
function_label = tk.Label(root, text="Функция:")
function_label.grid(column=1, row=0, pady=0, padx=0)
function_var = tk.StringVar(value="Выберите функцию")
function_dropdown = ttk.OptionMenu(root, function_var, "","Матьяса", "Экли", "Букин", "Розенброк")
function_dropdown.grid(column=1, row=1, pady=0, padx=0)

# Выбор метода оптимизации
method_label = tk.Label(root, text="Метод оптимизации:")
method_label.grid(column=2, row=0, pady=0, padx=0)
method_var = tk.StringVar(value="Выберите метод")
method_dropdown = ttk.OptionMenu(root, method_var, "", "Градиентный спуск", "Симплекс метод", "Генетический алгоритм","Роя частиц", "Пчелиный", "Имунной сети", "Бактериальный алгоритм", "Гибридный алгоритм")
method_dropdown.grid(column=2, row=1, pady=0, padx=0)

def callback(*args):
    if (method_var.get() == "Градиентный спуск"):
        gradient_GUI()
    if (method_var.get() == "Симплекс метод"):
        simplex_GUI()
    if (method_var.get() == "Генетический алгоритм"):
        genetic_GUI()
    if (method_var.get() == "Роя частиц"):
        particle_GUI()
    if (method_var.get() == "Пчелиный"):
        bees_GUI()
    if (method_var.get() == "Имунной сети"):
        imun_GUI()
    if (method_var.get() == "Бактериальный алгоритм"):
        bacteria_GUI()
    if (method_var.get() == "Гибридный алгоритм"):
        gibrid_GUI()

method_var.trace_add("write", callback)

points_var = tk.IntVar(value=100)
step_var = tk.DoubleVar(value=0.01)
X_var = tk.DoubleVar(value=3)
Y_var = tk.DoubleVar(value=3)

pers_var=tk.IntVar(value=20)
mutc_var=tk.DoubleVar(value=0.5)
mut_val=tk.DoubleVar(value=0.01)

iner_val = tk.StringVar(value=0.5)

scout_var = tk.StringVar(value=20)
perspective_bee_var = tk.StringVar(value=10)
best_bee_var = tk.StringVar(value=20)
perspective_var = tk.StringVar(value=3)
best_var = tk.StringVar(value=1)
size_var = tk.StringVar(value=0.5)


def genetic_GUI():

    points_label = tk.Label(root, text="Количество итераций:")
    points_label.grid(column=1, row=4, pady=0, padx=0)

    points_entry = ttk.Entry(root, textvariable=points_var)
    points_entry.grid(column=1, row=5, pady=0, padx=0)

    pers_label = tk.Label(root, text="Количество особей:")
    pers_label.grid(column=2, row=4, pady=0, padx=0)

    pers_entry = ttk.Entry(root, textvariable=pers_var)
    pers_entry.grid(column=2, row=5, pady=0, padx=0)

    mutc_label = tk.Label(root, text="Вероятность мутации:")
    mutc_label.grid(column=1, row=6, pady=0, padx=0)

    mutc_entry = ttk.Entry(root, textvariable=mutc_var)
    mutc_entry.grid(column=1, row=7, pady=0, padx=0)

    mut_label = tk.Label(root, text="Степень мутации:")
    mut_label.grid(column=2, row=6, pady=0, padx=0)

    mut_entry = ttk.Entry(root, textvariable=mut_val)
    mut_entry.grid(column=2, row=7, pady=0, padx=0)
    destroy_object = [points_label,points_entry,pers_label,pers_entry,mutc_label,mutc_entry,mut_label,mut_entry]


def gradient_GUI():

    points_label = tk.Label(root, text="Количество итераций:")
    points_label.grid(column=1, row=4, pady=0, padx=0)

    points_entry = ttk.Entry(root, textvariable=points_var)
    points_entry.grid(column=1, row=5, pady=0, padx=0)
    # Поле ввода для шага
    step_label = tk.Label(root, text="Шаг:")
    step_label.grid(column=2, row=4, pady=0, padx=0)

    step_entry = ttk.Entry(root, textvariable=step_var)
    step_entry.grid(column=2, row=5, pady=0, padx=0)
    # Поле ввода для начального X
    X_label = tk.Label(root, text="Начальный X:")
    X_label.grid(column=1, row=6, pady=0, padx=0)

    X_entry = ttk.Entry(root, textvariable=X_var)
    X_entry.grid(column=1, row=7, pady=0, padx=0)
    # Поле ввода для начального Y
    Y_label = tk.Label(root, text="Начальный Y:")
    Y_label.grid(column=2, row=6, pady=0, padx=0)
    Y_entry = ttk.Entry(root, textvariable=Y_var)
    Y_entry.grid(column=2, row=7, pady=0, padx=0)
    destroy_object = [points_label, points_entry, step_label, step_entry, X_label, X_entry, Y_label, Y_entry]
    def deleter(*args):
        for object_name in destroy_object:
            object_name.destroy()

    method_var.trace_add("write", deleter)

def simplex_GUI():
    
    X_label = tk.Label(root, text="Начальный X:")
    X_label.grid(column=1, row=4, pady=0, padx=0)

    X_entry = ttk.Entry(root, textvariable=X_var)
    X_entry.grid(column=1, row=5, pady=0, padx=0)
    # Поле ввода для начального Y
    Y_label = tk.Label(root, text="Начальный Y:")
    Y_label.grid(column=2, row=4, pady=0, padx=0)
    Y_entry = ttk.Entry(root, textvariable=Y_var)
    Y_entry.grid(column=2, row=5, pady=0, padx=0)
    destroy_object = [X_label, X_entry, Y_label, Y_entry]
    def deleter(*args):
        for object_name in destroy_object:
            object_name.destroy()

    method_var.trace_add("write", deleter)

def gibrid_GUI():

    points_label = tk.Label(root, text="Количество итераций:")
    points_label.grid(column=1, row=4, pady=0, padx=0)

    points_entry = ttk.Entry(root, textvariable=points_var)
    points_entry.grid(column=1, row=5, pady=0, padx=0)

    pers_label = tk.Label(root, text="Количество особей:")
    pers_label.grid(column=2, row=4, pady=0, padx=0)

    pers_entry = ttk.Entry(root, textvariable=pers_var)
    pers_entry.grid(column=2, row=5, pady=0, padx=0)

    mutc_label = tk.Label(root, text="Вероятность мутации:")
    mutc_label.grid(column=1, row=6, pady=0, padx=0)

    mutc_entry = ttk.Entry(root, textvariable=mutc_var)
    mutc_entry.grid(column=1, row=7, pady=0, padx=0)

    mut_label = tk.Label(root, text="Степень мутации:")
    mut_label.grid(column=2, row=6, pady=0, padx=0)

    mut_entry = ttk.Entry(root, textvariable=mut_val)
    mut_entry.grid(column=2, row=7, pady=0, padx=0)

    mutc_label = tk.Label(root, text="Степень инерции:")
    mutc_label.grid(column=1, row=8, pady=0, padx=0)

    mutc_entry = ttk.Entry(root, textvariable=mutc_var)
    mutc_entry.grid(column=1, row=9, pady=0, padx=0)

    destroy_object = [points_label,points_entry,pers_label,pers_entry,mutc_label,mutc_entry,mut_label,mut_entry]

    def deleter(*args):
        for object_name in destroy_object:
            object_name.destroy()

    method_var.trace_add("write", deleter)

def particle_GUI():

    points_label = tk.Label(root, text="Количество итераций:")
    points_label.grid(column=1, row=4, pady=0, padx=0)

    points_entry = ttk.Entry(root, textvariable=points_var)
    points_entry.grid(column=1, row=5, pady=0, padx=0)

    pers_label = tk.Label(root, text="Количество частиц:")
    pers_label.grid(column=2, row=4, pady=0, padx=0)

    pers_entry = ttk.Entry(root, textvariable=pers_var)
    pers_entry.grid(column=2, row=5, pady=0, padx=0)

    iner_label = tk.Label(root, text="Степень иннерции:")
    iner_label.grid(column=1, row=6, pady=0, padx=0)

    iner_entry = ttk.Entry(root, textvariable=iner_val)
    iner_entry.grid(column=1, row=7, pady=0, padx=0)
    destroy_object = [points_label, points_entry, pers_label, pers_entry, iner_label, iner_entry]

    def deleter(*args):
        for object_name in destroy_object:
            object_name.destroy()

    method_var.trace_add("write", deleter)

def bees_GUI():
    points_label = tk.Label(root, text="Кол-во итераций:")
    points_label.grid(column=1, row=4, pady=0, padx=0)

    points_entry = ttk.Entry(root, textvariable=points_var)
    points_entry.grid(column=1, row=5, pady=0, padx=0)

    scout_label = tk.Label(root, text="Кол-во разведчиков:")
    scout_label.grid(column=2, row=4, pady=0, padx=0)

    scout_entry = ttk.Entry(root, textvariable=scout_var)
    scout_entry.grid(column=2, row=5, pady=0, padx=0)

    perspective_bee_label = tk.Label(root, text="Пчел на перспективном участке:")
    perspective_bee_label.grid(column=1, row=6, pady=0, padx=0)

    perspective_bee_entry = ttk.Entry(root, textvariable=perspective_bee_var)
    perspective_bee_entry.grid(column=1, row=7, pady=0, padx=0)

    best_bee_label = tk.Label(root, text="Пчел на лучшем участке:")
    best_bee_label.grid(column=2, row=6, pady=0, padx=0)

    best_bee_entry = ttk.Entry(root, textvariable=best_bee_var)
    best_bee_entry.grid(column=2, row=7, pady=0, padx=0)

    destroy_object = [points_label, points_entry, scout_label, scout_entry, perspective_bee_label, perspective_bee_entry,best_bee_label,best_bee_entry]

    def deleter(*args):
        for object_name in destroy_object:
            object_name.destroy()

    method_var.trace_add("write", deleter)

def imun_GUI():
    function_var.set("Розенброк")
    points_label = tk.Label(root, text="Количество итераций:")
    points_label.grid(column=1, row=4, pady=0, padx=0)

    points_entry = ttk.Entry(root, textvariable=points_var)
    points_entry.grid(column=1, row=5, pady=0, padx=0)

    pers_label = tk.Label(root, text="Количество антител:")
    pers_label.grid(column=2, row=4, pady=0, padx=0)

    pers_entry = ttk.Entry(root, textvariable=[pers_var])
    pers_entry.grid(column=2, row=5, pady=0, padx=0)

    best_imun_label = tk.Label(root, text="Количество лучших отбираемых:")
    best_imun_label.grid(column=1, row=6, pady=0, padx=0)

    best_imun_entry = ttk.Entry(root, textvariable=best_imun_var)
    best_imun_entry.grid(column=1, row=7, pady=0, padx=0)

    clons_label = tk.Label(root, text="Количество клонов:")
    clons_label.grid(column=2, row=6, pady=0, padx=0)

    clons_entry = ttk.Entry(root, textvariable=clons_var)
    clons_entry.grid(column=2, row=7, pady=0, padx=0)

    destroy_object = [points_label, points_entry, pers_label,pers_entry,best_imun_label,best_imun_entry,clons_label,clons_entry]

    def deleter(*args):
        for object_name in destroy_object:
            object_name.destroy()

    method_var.trace_add("write", deleter)


hemotaxis_var=tk.IntVar(value=6)
elimination_var=tk.IntVar(value=15)

def bacteria_GUI():

    points_label = tk.Label(root, text="Кол-во итераций:")
    points_label.grid(column=1, row=4, pady=0, padx=0)

    points_entry = ttk.Entry(root, textvariable=points_var)
    points_entry.grid(column=1, row=5, pady=0, padx=0)

    pers_label = tk.Label(root, text="Количество особей:")
    pers_label.grid(column=1, row=6, pady=0, padx=0)
    
    pers_entry = ttk.Entry(root, textvariable=pers_var)
    pers_entry.grid(column=1, row=7, pady=0, padx=0)
    
    hemotax_label = tk.Label(root, text="Шаги хемотаксиса:")
    hemotax_label.grid(column=2, row=4, pady=0, padx=0)

    hemotax_entry = ttk.Entry(root, textvariable=hemotaxis_var)
    hemotax_entry.grid(column=2, row=5, pady=0, padx=0)
    
    elim_label = tk.Label(root, text="Вероятность ликвидации:")
    elim_label.grid(column=2, row=6, pady=0, padx=0)
    
    elim_entry = ttk.Entry(root, textvariable=elimination_var)
    elim_entry.grid(column=2, row=7, pady=0, padx=0)

    destroy_object = [points_label,points_entry,pers_label,pers_entry,hemotax_label,hemotax_entry,elim_label,elim_entry]
    
    def deleter(*args):
        for object_name in destroy_object:
            object_name.destroy()
    
    method_var.trace_add("write", deleter)

# Функция, вызываемая при нажатии кнопки "Визуализировать"
def visualize():
    # Получение выбранной функции, метода оптимизации и количества точек
    selected_function = function_var.get()
    selected_method = method_var.get()

        # Определение функции и градиента
    if selected_function == "Букин":
        function = bukin_function
        gradient = gradient_bukin
    elif selected_function == "Матьяса":
        function = matyas_function
        gradient = gradient_matyas
    elif selected_function == "Экли":
        function = ackley_function
        gradient = gradient_ackley
    elif selected_function == "lr2Func":
        function = lr2Function
    elif selected_function == "Розенброк":
        function = rosenbrock
    else:
        messagebox.showerror("Выберите другую функцию")
        return

    # Создание сетки значений
    x = np.linspace(-5, 5, 500)
    y = np.linspace(-5, 5, 500)
    X, Y = np.meshgrid(x, y)
    Z = function(X, Y)

    # Рисование функции
    ax.cla()
    ax.plot_surface(X, Y, Z, cmap=cm.ocean, alpha=0.8)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(selected_function)
    ax.view_init(elev=30, azim=60)

    if selected_method == "Градиентный спуск":

        num_iter = points_var.get()

        # Очистка текстового поля
        points_text.delete("1.0", tk.END)

        # Начальные значения
        xi = X_var.get()
        yi = Y_var.get()
        fi = function(xi, yi)
        step = step_var.get()
        num_iterations = num_iter

        # Градиентный спуск
        point = ax.scatter(xi, yi, function(np.array(xi), np.array(yi)), c='r', alpha=1.0)
        canvas.draw()
        root.update()
        for i in range(num_iterations - 1):
            xip, yip, fip = xi, yi, fi
            point.remove()
            grad_x, grad_y = gradient(xi, yi)
            xi = xi - step * grad_x
            yi = yi - step * grad_y
            fi = function(xi, yi)
            point = ax.scatter(xi, yi, fi, c='r', alpha=1.0)
            points_text.insert(tk.END, f"Итерация {i + 1}:({xi:.4f}, {yi:.4f}) f= {fi:.4f}\n")
            canvas.draw()
            root.update()
            if np.sqrt((xi - xip) ** 2 + (yi - yip) ** 2) < 0.0001 and abs(fi - fip) < 0.0001:
                break
            time.sleep(0.1)
        points_text.insert(tk.END, f"Итог ({xi:.4f}, {yi:.4f})\n f= {fi:.4f}")

    parc=3

    def generate_pop(pers):
        population = [[0] * 3 for i in range(pers)]
        popv=-5
        for i in range(pers):
            population[i][1]=popv
            population[i][2]=popv
            population[i][0]=rosenbrock(population[i][0],population[i][1])
            popv+=10/pers
        return population

    def selection(population,pers,mut_coef,mut_val):
        population.sort()
        parents=population[0:parc]
        newpop=population
        for i in range(1,pers):
            newpop[i][1]=parents[int(uniform(0,parc-1))][1]
            newpop[i][2]=parents[int(uniform(0,parc-1))][2]
            if random.random() < mut_coef:
                newpop[i][1]+=mut_val
            if random.random() < mut_coef:
                newpop[i][2]+=mut_val
            newpop[i][0]=rosenbrock(newpop[i][1],newpop[i][2])
        return newpop

    if selected_method=="Генетический алгоритм":
        
        points_text.delete("1.0", tk.END)
        canvas.draw()
        pers_count=pers_var.get()
        iters=points_var.get()
        mutc=mutc_var.get()
        mutv=mut_val.get()
        pop=generate_pop(pers_count)
        points=[]
        for t in range(pers_count):
            point=ax.scatter(pop[t][1],pop[t][2],rosenbrock(pop[t][1],pop[t][2]),c='black',alpha=0.3)
            points.append(point)
        canvas.draw()
        root.update()
        time.sleep(0.025)
        for point in points:
            point.remove()
        for i in range(iters):
            pop=selection(pop,pers_count,mutc,mutv)
            points = []
            point = ax.scatter(pop[0][1], pop[0][2], rosenbrock(pop[0][1], pop[0][2])+10, c='red', alpha=1.0)
            points.append(point)
            points_text.insert(tk.END, f"{i+1}. (x= {pop[0][1]:.4f}, y= {pop[0][2]:.4f}) f= {pop[0][0]:.4f}\n")
            for j in range(1,pers_count):
                point = ax.scatter(pop[j][1], pop[j][2], rosenbrock(pop[j][1], pop[j][2]), c='black', alpha=0.1)
                points.append(point)
            canvas.draw()
            root.update()
            time.sleep(0.025)
            if(i!=iters-1):
                for point in points:
                    point.remove()

    if selected_method == "Бактериальный алгоритм":
        # ewtgb = 3 + 5

        pers_count = pers_var.get()
        iters = points_var.get()
        elimc=elimination_var.get()/100

        hemotax_step=hemotaxis_var.get()
        pop=[[0] * 4 for i in range(pers_count)]
 
        for i in range(pers_count):
            pop[i][1]=uniform(-5,5)
            pop[i][2]=uniform(-5,5)
            pop[i][0]=function(pop[i][1],pop[i][2])
            pop[i][3]=pop[i][0]
 

        points = []
        for a in range(len(pop)):
            point = ax.scatter(pop[a][1], pop[a][2], function(pop[a][1], pop[a][2]), c='black', alpha=0.3)
            points.append(point)
            
        point = ax.scatter(pop[0][1], pop[0][2], function(pop[0][1], pop[0][2]), c='red', alpha=1)
        points.append(point)
        canvas.draw()
        root.update()
        time.sleep(0.025)
        points_text.insert(tk.END, f"{0}. (x= {pop[0][1]:.4f}, y= {pop[0][2]:.4f}) f= {pop[0][0]:.4f}\n")
        
        for i in range(iters):
            for point in points:
                point.remove()
                
            coef=1/(i+1)
            for bac in pop:
                vec = [coef * random.uniform(-1, 1), coef * random.uniform(-1, 1)]
                for _ in range(hemotax_step):
                    f = bac[0]
                    
                    bac[1] += vec[0]  # X
                    bac[2] += vec[1]  # Y
                    bac[0] = function(bac[1], bac[2])  # Z / Фитнес-Функция
                    bac[3] += bac[0]  # Health
                    
                    if f < bac[3]:
                        vec = [coef * random.uniform(-1, 1), coef * random.uniform(-1, 1)]

            pop.sort()
            for j in range(len(pop) // 2):
                pop[len(pop) // 2 + j] = pop[j].copy()
                
            for bac in pop:
                if random.uniform(0, 1) <= elimc:
                    bac[1] = random.uniform(-5, 5)
                    bac[2] = random.uniform(-5, 5)
                    bac[0] = function(bac[0], bac[1])
                    bac[3] = bac[0]
                    
            pop.sort()
            points = []
            for a in range(len(pop)):
                point = ax.scatter(pop[a][1], pop[a][2], function(pop[a][1], pop[a][2]), c='black', alpha=0.3)
                points.append(point)
            point = ax.scatter(pop[0][1], pop[0][2], pop[0][0], c='red', alpha=1)
            points.append(point)
            
            time.sleep(0.025)

            points_text.insert(tk.END, f"{i+1}. (x= {pop[0][1]:.4f}, y= {pop[0][2]:.4f}) f= {pop[0][0]:.4f}\n")
            canvas.draw()
            root.update()

    if selected_method == "Симплекс метод":
        points_text.delete("1.0", tk.END)

        def lr2Function(x_i):
            x1 = x_i[0]
            x2 = x_i[1]
            return 2 * x1 * x1 + 3 * x2 * x2 + 4 * x1 * x2 - 6 * x1 - 3 * x2

        canvas.draw()
        x_start = 5
        y_start = 5

        x0 = np.array([x_start, y_start])
        point = ax.scatter(x0[0], x0[1], function(x0[0], x0[1]), c='r', alpha=1.0)
        point.remove()

        def saver(xk):
            point = ax.scatter(xk[0], xk[1], function(xk[0], xk[1]), c='r', alpha=1.0)
            points_text.insert(tk.END, f"({xk[0]:.4f}, {xk[1]:.4f}) f= {function(xk[0], xk[1]):.4f}\n")
            canvas.draw()
            time.sleep(0.3)
            point.remove()

        b = (0, float("inf"))
        bounds = (b, b)
        min_res = minimize(lr2Function, x0, method="SLSQP", bounds=bounds, constraints={'type': 'eq', 'fun': lr2Function},
                           callback=saver)
        point = ax.scatter(min_res['x'][0], min_res['x'][1], function(min_res['x'][0], min_res['x'][1]), c='r',
                           alpha=1.0)

    if selected_method=="Роя частиц":
        points_text.delete("1.0", tk.END)
        canvas.draw()
        n_ind=pers_var.get()
        n_point=points_var.get()
        alpha=0.8
        beta=0.9
        inner=float(iner_val.get())

        def new_vec(r, b, gt):
            for i in range(n_ind):
                r[i][3] = inner * r[i][3] + alpha * uniform(0, 1) * (b[i][1] - r[i][1]) + beta * uniform(0, 1) * (gt[1] - r[i][1])
                r[i][4] = inner * r[i][4] + alpha * uniform(0, 1) * (b[i][2] - r[i][2]) + beta * uniform(0, 1) * (gt[2] - r[i][2])
            return r

        def new_point(roy):
            for i in range(n_ind):
                roy[i][1] += roy[i][3]
                roy[i][2] += roy[i][4]
                roy[i][0] = function(roy[i][1], roy[i][2])
            return roy

        roy = [[0] * 5 for i in range(n_ind)]
        for i in range(n_ind):
            roy[i][3] = uniform(-1, 1)
            roy[i][4] = uniform(-1, 1)
            roy[i][1] = uniform(-5, 5)
            roy[i][2] = uniform(-5, 5)
            roy[i][0] = function(roy[i][0], roy[i][1])
        points = []
        best_point_for_all = roy[0]
        for i in range(n_ind):
            if roy[i][0] < best_point_for_all[0]:
                best_point_for_all = roy[i]
            point = ax.scatter(roy[i][1], roy[i][2], function(roy[i][1], roy[i][2]), c="r", alpha=0.3)
            points.append(point)
        p_best = [[0] * 3 for i in range(n_ind)]
        for i in range(n_ind):
            p_best[i][0] = roy[i][0]
            p_best[i][1] = roy[i][1]
            p_best[i][2] = roy[i][2]
        points_text.insert(tk.END,f"1. x= {best_point_for_all[1]:.4f}, y= {best_point_for_all[2]:.4f} f= {best_point_for_all[0]:.4f}\n")
        canvas.draw()
        root.update()
        time.sleep(0.01)
        for point in points:
            point.remove()
        for i in range(1, n_point):
            roy = new_vec(roy, p_best, best_point_for_all)
            roy = new_point(roy)
            points = []
            for j in range(n_ind):
                if roy[j][0] < best_point_for_all[0]:
                    best_point_for_all = roy[j]
                point = ax.scatter(roy[j][1], roy[j][2], function(roy[j][1], roy[j][2]), c="r", alpha=0.3)
                points.append(point)
            points_text.insert(tk.END,f"{i+1}. x= {best_point_for_all[1]:.4f}, y= {best_point_for_all[2]:.4f} f= {best_point_for_all[0]:.4f}\n")

            for j in range(n_ind):
                if p_best[j][0] > roy[j][0]:
                    p_best[j][0] = roy[j][0]
                    p_best[j][1] = roy[j][1]
                    p_best[j][2] = roy[j][2]
            canvas.draw()
            root.update()
            time.sleep(0.01)
            if i != n_point - 1:
                for point in points:
                    point.remove()

    if selected_method=="Пчелиный":

        n_point = int(points_var.get())
        n_scout = int(scout_var.get())
        n_perspective_bee = int(perspective_bee_var.get())
        n_best_bee = int(best_bee_var.get())
        n_perspective = int(perspective_var.get())
        n_best = int(best_var.get())
        size = float(size_var.get())

        def scout_spawn(n_scout):
            scouts = [[0] * 3 for i in range(n_scout)]
            for i in range(n_scout):
                scouts[i][1] = uniform(-5, 5)
                scouts[i][2] = uniform(-5, 5)
                scouts[i][0] = function(scouts[i][1], scouts[i][2])
            return scouts

        def best_bee_spawn(bp, n_best_bee, size):
            bb = [[0] * 3 for i in range(n_best_bee)]
            bb[0][1] = bp[1]
            bb[0][2] = bp[2]
            bb[0][0] = function(bb[0][1], bb[0][2])
            for i in range(1, n_best_bee):
                bb[i][1] = bp[1] + uniform(-size, size)
                bb[i][2] = bp[2] + uniform(-size, size)
                bb[i][0] = function(bb[i][1], bb[i][2])
            return bb

        def perspective_bee_spawn(pp, n_perspective_bee, size):
            pb = [[0] * 3 for i in range(n_perspective_bee)]
            pb[0][1] = pp[1]
            pb[0][2] = pp[2]
            pb[0][0] = function(pb[0][1], pb[0][2])
            for i in range(1, n_perspective_bee):
                pb[i][1] = pp[1] + uniform(-size, size)
                pb[i][2] = pp[2] + uniform(-size, size)
                pb[i][0] = function(pb[i][1], pb[i][2])
            return pb

        scouts = scout_spawn(n_scout)
        points = []
        for i in range(n_scout):
            point = ax.scatter(scouts[i][1], scouts[i][2], function(scouts[i][1], scouts[i][2]), c="b", alpha=0.3)
            points.append(point)
        scouts.sort()
        points_text.insert(tk.END, f"0. x= {scouts[0][1]:.4f}, y= {scouts[0][2]:.4f} f= {scouts[0][0]:.4f}\n")
        canvas.draw()
        root.update()
        time.sleep(0.01)
        best_point = []
        perspective_point = []
        for i in range(n_best):
            best_point.append(scouts[i])
        for i in range(n_best, n_best + n_perspective):
            perspective_point.append(scouts[i])
        for point in points:
            point.remove()

        for i in range(n_point):
            points = []
            best_bee = [[0] for i in range(n_best)]
            perspective_bee = [[0] for i in range(n_perspective)]
            for j in range(n_best):
                best_bee[j] = best_bee_spawn(best_point[j], n_best_bee, size)
            for j in range(n_perspective):
                perspective_bee[j] = perspective_bee_spawn(perspective_point[j], n_perspective_bee, size)
            scouts = scout_spawn(n_scout)

            for j in range(n_scout):
                point = ax.scatter(scouts[j][1], scouts[j][2], function(scouts[j][1], scouts[j][2]), c="b", alpha=0.3)
                points.append(point)
            for j in range(n_best):
                for q in range(n_best_bee):
                    point = ax.scatter(best_bee[j][q][1], best_bee[j][q][2],
                                        function(best_bee[j][q][1], best_bee[j][q][2]), c="b", alpha=0.3)
                    points.append(point)
            for j in range(n_perspective):
                for q in range(n_perspective_bee):
                    point = ax.scatter(perspective_bee[j][q][1], perspective_bee[j][q][2],
                                        function(perspective_bee[j][q][1], perspective_bee[j][q][2]), c="b", alpha=0.3)
                    points.append(point)

            b = []
            for j in range(n_perspective):
                b.extend(perspective_bee[j])
            for j in range(n_best):
                b.extend(best_bee[j])
            for j in range(n_scout):
                b.extend(scouts)

            b.sort()

            best_point = []
            perspective_point = []
            for j in range(n_best):
                best_point.append(b[j])
            for j in range(n_best, n_best + n_perspective):
                perspective_point.append(b[j])

            point = ax.scatter(best_point[0][1], best_point[0][2], function(best_point[0][1], best_point[0][2]), c="r",
                                alpha=1)
            points.append(point)
            points_text.insert(tk.END,f"{i+1}. x= {best_point[0][1]:.4f}, y= {best_point[0][2]:.4f} f= {best_point[0][0]:.4f}\n")
            canvas.draw()
            root.update()
            time.sleep(0.001)
            if i != n_point - 1:
                for point in points:
                    point.remove()

    if selected_method == "Имунной сети":
        pers_count = pers_var.get()
        iters = points_var.get()
        best_count=best_imun_var.get()
        clons_count=clons_var.get()
        pop=[[0] * 3 for i in range(pers_count)]
        for i in range(pers_count):
            pop[i][1]=uniform(-5,5)
            pop[i][2]=uniform(-5,5)
            pop[i][0]=function(pop[i][1],pop[i][2])
        pop.sort()
        for j in range(iters):
            points = []
            for a in range(len(pop)):
                point = ax.scatter(pop[a][1], pop[a][2], function(pop[a][1], pop[a][2]), c='black', alpha=0.3)
                points.append(point)
            point = ax.scatter(pop[0][1], pop[0][2], function(pop[0][1], pop[0][2]), c='red', alpha=1)
            points.append(point)
            canvas.draw()
            root.update()
            clons=[]
            for t in range(clons_count):
                clons.append(pop[int((t//(clons_count/best_count)))])
            clonsn=[[0] * 3 for i in range(clons_count)]
            for z in range(len(clons)):
                #print(z)
                clonsn[z][1] = clons[z][1]+random.uniform(-0.5,0.5)*(2/(j+1))
                clonsn[z][2] = clons[z][2]+random.uniform(-0.5, 0.5)*(2/(j+1))
                clonsn[z][0] = function(clons[z][1],clons[z][2])
            pop=pop+clonsn
            pop.sort()
            pop=pop[0:pers_count//2]
            popn=[[0] * 3 for i in range(pers_count//2)]
            for v in range(pers_count//2):
                popn[v][1] = uniform(-5, 5)
                popn[v][2] = uniform(-5, 5)
                popn[v][0] = function(popn[v][1], popn[v][2])

            if j != iters-1:
                #print(j,len(pop)-1)
                for point in points:
                    point.remove()

            for aboba in popn:
                pop.append(aboba)
            pop.sort()
            time.sleep(0.025)
            points_text.insert(tk.END, f"{j+1}. (x= {pop[0][1]:.4f}, y= {pop[0][2]:.4f}) f= {pop[0][0]:.4f}\n")
            canvas.draw()
            root.update()

    parc=3

    def generate_pop(pers):
        population = [[0] * 3 for i in range(pers)]
        popv=-5
        for i in range(pers):
            population[i][1]=popv
            population[i][2]=popv
            population[i][0]=rosenbrock(population[i][0],population[i][1])
            popv+=10/pers
        return population

    def selection(population,pers,mut_coef,mut_val):
        population.sort()
        parents=population[0:parc]
        newpop=population
        for i in range(1,pers):
            newpop[i][1]=parents[int(uniform(0,parc-1))][1]
            newpop[i][2]=parents[int(uniform(0,parc-1))][2]
            if random.random() < mut_coef:
                newpop[i][1]+=mut_val
            if random.random() < mut_coef:
                newpop[i][2]+=mut_val
            newpop[i][0]=rosenbrock(newpop[i][1],newpop[i][2])
        return newpop

    if selected_method=="Гибридный алгоритм":
        
        points_text.delete("1.0", tk.END)
        canvas.draw()
        pers_count=pers_var.get()
        iters=points_var.get()
        mutc=mutc_var.get()
        mutv=mut_val.get()
        pop=generate_pop(pers_count)
        points=[]
        for t in range(pers_count):
            point=ax.scatter(pop[t][1],pop[t][2],rosenbrock(pop[t][1],pop[t][2]),c='black',alpha=0.3)
            points.append(point)
        canvas.draw()
        root.update()
        time.sleep(0.025)
        for point in points:
            point.remove()
        for i in range(iters):
            pop=selection(pop,pers_count,mutc,mutv)
            points = []
            point = ax.scatter(pop[0][1], pop[0][2], rosenbrock(pop[0][1], pop[0][2])+10, c='red', alpha=1.0)
            points.append(point)
            points_text.insert(tk.END, f"{i+1}. (x= {pop[0][1]:.4f}, y= {pop[0][2]:.4f}) f= {pop[0][0]:.4f}\n")
            for j in range(1,pers_count):
                point = ax.scatter(pop[j][1], pop[j][2], rosenbrock(pop[j][1], pop[j][2]), c='black', alpha=0.1)
                points.append(point)
            canvas.draw()
            root.update()
            if(i!=iters-1):
                for point in points:
                    point.remove()

        canvas.draw()
        n_ind=pers_count
        n_point=iters
        alpha=0.8
        beta=0.9
        inner=float(iner_val.get())

        def new_vec(r, b, gt):
            for i in range(n_ind):
                r[i][3] = inner * r[i][3] + alpha * uniform(0, 1) * (b[i][1] - r[i][1]) + beta * uniform(0, 1) * (gt[1] - r[i][1])
                r[i][4] = inner * r[i][4] + alpha * uniform(0, 1) * (b[i][2] - r[i][2]) + beta * uniform(0, 1) * (gt[2] - r[i][2])
            return r

        def new_point(roy):
            for i in range(n_ind):
                roy[i][1] += roy[i][3]
                roy[i][2] += roy[i][4]
                roy[i][0] = function(roy[i][1], roy[i][2])
            return roy

        roy = [[0] * 5 for i in range(n_ind)]
        for i in range(n_ind):
            roy[i][3] = uniform(-1, 1)
            roy[i][4] = uniform(-1, 1)
            roy[i][1] = uniform(-5, 5)
            roy[i][2] = uniform(-5, 5)
            roy[i][0] = function(roy[i][0], roy[i][1])
        points = []
        best_point_for_all = roy[0]
        for i in range(n_ind):
            if roy[i][0] < best_point_for_all[0]:
                best_point_for_all = roy[i]
            point = ax.scatter(roy[i][1], roy[i][2], function(roy[i][1], roy[i][2]), c="r", alpha=0.3)
            points.append(point)
        p_best = [[0] * 3 for i in range(n_ind)]
        for i in range(n_ind):
            p_best[i][0] = roy[i][0]
            p_best[i][1] = roy[i][1]
            p_best[i][2] = roy[i][2]
        points_text.insert(tk.END,f"1. x= {best_point_for_all[1]:.4f}, y= {best_point_for_all[2]:.4f} f= {best_point_for_all[0]:.4f}\n")
        canvas.draw()
        root.update()
        time.sleep(0.01)
        for point in points:
            point.remove()
        for i in range(1, n_point):
            roy = new_vec(roy, p_best, best_point_for_all)
            roy = new_point(roy)
            points = []
            for j in range(n_ind):
                if roy[j][0] < best_point_for_all[0]:
                    best_point_for_all = roy[j]
                point = ax.scatter(roy[j][1], roy[j][2], function(roy[j][1], roy[j][2]), c="r", alpha=0.3)
                points.append(point)
            points_text.insert(tk.END,f"{i+1}. x= {best_point_for_all[1]:.4f}, y= {best_point_for_all[2]:.4f} f= {best_point_for_all[0]:.4f}\n")

            for j in range(n_ind):
                if p_best[j][0] > roy[j][0]:
                    p_best[j][0] = roy[j][0]
                    p_best[j][1] = roy[j][1]
                    p_best[j][2] = roy[j][2]
            canvas.draw()
            root.update()
            time.sleep(0.01)
            if i != n_point - 1:
                for point in points:
                    point.remove()
# Кнопка "Визуализировать"
visualize_button = tk.Button(root, text="Визуализировать", command=visualize)
visualize_button.grid(column=1, row=12, pady=0, padx=0)

# Текстовое поле для вывода точек
result_label = tk.Label(root, text="Выполнение и результаты")
result_label.grid(column=1, row=14, sticky='w')  # Расположение лейбла
points_text = tk.Text(root, height=10, width=25)
points_text.grid(column=1, row=13, pady=0, padx=0)

# Запуск GUI
root.mainloop()
