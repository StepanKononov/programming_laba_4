from tkinter import *
import yfinance as yf
from tkinter import ttk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from tkcalendar import DateEntry
from datetime import datetime

t = []
for x in list(range(0, 101)):
    t.append(x / 10)


def main():
    root = Tk()
    gui = Window(root)
    gui.root.mainloop()
    return None


class Window:
    def __init__(self, root):
        self.select_deviation = None
        self.select_start_date = None
        self.select_finish_date = None
        self.select_ticker = None
        self.select_anti_aliasing = None
        self.select_data_recovery = None
        self.select_time_interval = None
        self.interval = None

        def row_generator(number):
            i = 0
            while i < number:
                yield i
                i += 1

        row = row_generator(20)
        self.root = root
        self.root.title("Sin Wave")
        self.root.geometry('600x550')
        self.root.resizable(False, False)

        # Тикеры скачиваем из файла
        tik_f = open('tiker.txt')
        self.tickers = list((tik_f.readline().split()))
        # Доступные интервалы времени и текущий интервал
        self.intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']


        # Доступные методы востановления данных
        self.data_recovery_methods = ['Winsoring', 'L-approx', 'C-recovery']
        # Доступные методы сглаживания данных
        self.anti_aliasing_methods = ['MA', 'WMA']
        # Доступные отклонения
        self.deviations = [str(i) + '%' for i in range(0, 105, 5)]

        width = 10

        # Тикеры
        r = next(row)
        Label(self.root, text="Тикер").grid(row=r, column=0)
        self.tikcer_entry = ttk.Combobox(self.root, width=width, values=self.tickers)
        self.tikcer_entry.current(0)
        self.tikcer_entry.grid(row=r, column=1)

        # Временной период взятия данных
        r = next(row)
        Label(self.root, text="Временной период").grid(row=r, column=0)
        self.time_interval_entry = ttk.Combobox(self.root, width=width, values=self.intervals)
        self.time_interval_entry.current(8)
        self.time_interval_entry.grid(row=r, column=1)

        # Начальньная дата
        r = next(row)
        Label(self.root, text="Начальньная дата").grid(row=r, column=0)
        self.start_date_entry = DateEntry(self.root, width=width, bg="darkblue", fg="white", year=2011)
        self.start_date_entry.grid(row=r, column=1)

        # Конечная дата
        r = next(row)
        Label(self.root, text="Конечная дата").grid(row=r, column=0)
        self.finish_date_entry = DateEntry(self.root, width=width, bg="darkblue", fg="white", year=2012)
        self.finish_date_entry.grid(row=r, column=1)

        # Методы востановления данных
        r = next(row)
        Label(self.root, text="Методы востановления данных").grid(row=r, column=0)
        self.data_recovery_entry = ttk.Combobox(self.root, width=width, values=self.data_recovery_methods)
        self.data_recovery_entry.current(0)
        self.data_recovery_entry.grid(row=r, column=1)

        # Доступные методы сглаживания
        r = next(row)
        Label(self.root, text="Методы сглаживания").grid(row=r, column=0)
        self.anti_aliasing_entry = ttk.Combobox(self.root, width=width, values=self.anti_aliasing_methods)
        self.anti_aliasing_entry.current(0)
        self.anti_aliasing_entry.grid(row=r, column=1)

        # Допустимое отклонение
        r = next(row)
        Label(self.root, text="Допустимое отклонение (%)").grid(row=r, column=0)
        self.deviation_entry = ttk.Combobox(self.root, width=width, values=self.deviations)
        self.deviation_entry.current(0)
        self.deviation_entry.grid(row=r, column=1)

        # Update Button
        r = next(row)
        button1 = Button(self.root, text="Calculate", command=self.update_values)
        button1.grid(row=r , column=0)
        self.root.bind("<Return>", self.update_values)
       # self.root.rowconfigure(r, weight=2)

        self.update_values()

    def update_values(self, event=None):
        self.select_ticker = self.tikcer_entry.get()
        self.select_anti_aliasing = self.anti_aliasing_entry.get()
        self.select_data_recovery = self.data_recovery_entry.get()
        self.select_time_interval = self.time_interval_entry.get()
        self.select_start_date = str(datetime.strptime(self.start_date_entry.get(), '%m/%d/%y'))[:10]
        self.select_finish_date = str(datetime.strptime(self.finish_date_entry.get(), '%m/%d/%y'))[:10]
        self.select_deviation = self.deviation_entry.get()


        print(self.select_ticker, self.select_anti_aliasing, self.select_data_recovery, self.select_time_interval, self.select_start_date, self.select_finish_date, self.select_deviation)
        self.plot_values()

    def get_data(self, startDate, endDate, interval):
        shares_data_t = dict()
        for ticker in self.tickers:
            data = yf.Ticker(ticker)
            shares_data_t[ticker] = list(data.history(start=startDate, end=endDate, interval=interval)['Close'])
        return shares_data_t

    def plot_values(self):
        """
        plt.close('all')
        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)

        x = np.linspace(-5, 5, 100)

        y = np.cos(x)

        plt.plot(x, y)

        ax.spines['left'].set_position('center')
        ax.spines['bottom'].set_position('center')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        chart = FigureCanvasTkAgg(fig, self.root)

        chart.get_tk_widget().grid(row=10, column=0, columnspan=2, stick='we')

        """
        plt.close('all')
        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)

        y = self.get_data(self.select_start_date,  self.select_finish_date,   self.select_time_interval)[self.select_ticker]
        x = [i for i in range(len(y))]

        print(y)
        print(x)
        plt.plot(x, y)
        chart = FigureCanvasTkAgg(fig, self.root)
        chart.get_tk_widget().grid(row=10, column=0, columnspan=2, stick='we')


main()
