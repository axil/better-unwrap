import sys
from math import pi     
 
import numpy as np                                               
from scipy.constants import c

from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtCore import pyqtSlot as slot
import pyqtgraph as pg

# по умолчанию фон графиков pyqtgraph чёрный, делаем его белым
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

Design, _ = uic.loadUiType('design.ui') # Подгружаем список виджетов из design.ui


import pandas as pd
df1 = pd.read_csv('reference signal.lvm', sep='\t', skiprows=21, decimal=',')
df2 = pd.read_csv('silicon wafer signal.lvm', sep='\t', skiprows=21, decimal=',')
r = df1.scan 
s = df2.scan[:len(r)]
ftt_E_1 = np.fft.fft(df1['scan'])
freq_1 = np.fft.fftfreq(len(ftt_E_1), df1['X_Value'][1] - df1['X_Value'][0])

def calc_y(r, v=-141, xmin=170, xmax=190):
    return np.unwrap(np.angle(np.fft.fft(np.roll(r, v))))[xmin:xmax]#-v*np.linspace(0, 2*pi, len(r))

def calc_n(r, s, dr=-141, ds=-305, xmin=170, xmax=190):
    ur = np.unwrap(np.angle(np.fft.fft(np.roll(r, dr))))+dr*np.linspace(0, 2*pi, len(r))
    us = np.unwrap(np.angle(np.fft.fft(np.roll(s, ds))))+ds*np.linspace(0, 2*pi, len(s))
    delta_ang = us - ur
    n = (1-(c*delta_ang[1:]/(freq_1[1:]*2.08/1000*6.28)))
#    return freq_1[:len(freq_1)//2], n1[:len(freq_1)//2]
#    return np.unwrap(np.angle(np.fft.fft(np.roll(r, v))))[xmin:xmax]#-v*np.linspace(0, 2*pi, len(r))
    return freq_1[xmin:xmax], n[xmin:xmax]

class ExampleApp(QtWidgets.QMainWindow, Design):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Этот метод из класса Design, он инициализирует виджеты
        self.x = np.arange(len(r))
        minv, maxv, dr, ds = -200, 0, -141, -305
        y = calc_y(r)
        t, n = calc_n(r, s)
        self.curve1 = self.canvas1.plot(y, pen=(31, 119, 180))
        self.curve2 = self.canvas2.plot(n, pen=(31, 119, 180))
        self.curve3 = self.canvas3.plot(n, pen=(31, 119, 180))
        self.v.setMinimum(minv)
        self.v.setMaximum(maxv)
        self.v.setValue(v)
        self.v_slider.setMinimum(minv)
        self.v_slider.setMaximum(maxv)
        self.v_slider.setValue(v)

 
    def update(self, v=None, xmin=None, xmax=None):
        if v is None:
            v = self.v.value()
        if xmin is None:
            xmin = self.xmin.value()
        if xmax is None:
            xmax = self.xmax.value()
        y = calc_y(r, v, xmin, xmax)
        self.curve1.setData(y)
        t, n = calc_n(r, s, dr=v, xmin=xmin, xmax=xmax)
        self.curve2.setData(n)

    @slot(int)
    def on_v_valueChanged(self, v):
        self.update(v=v)

    @slot(int)
    def on_xmin_valueChanged(self, xmin):
        self.update(xmin=xmin)

    @slot(int)
    def on_xmax_valueChanged(self, xmax):
        self.update(xmax=xmax)

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))   # Более современная тема оформления
    app.setPalette(QtWidgets.QApplication.style().standardPalette())  # Берём цвета из темы оформления
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
