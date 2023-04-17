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
    ur -= ur[0]
    us = np.unwrap(np.angle(np.fft.fft(np.roll(s, ds))))+ds*np.linspace(0, 2*pi, len(s))
    us -= us[0]
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
        minv, maxv, dr, ds = -400, 0, -141, -305
        y = calc_y(r)
        t, n = calc_n(r, s, dr=dr, ds=ds)
        self.curve1 = self.canvas1.plot(y, pen=(31, 119, 180))
        self.curve2 = self.canvas2.plot(n, pen=(31, 119, 180))
        self.curve3 = self.canvas3.plot(n, pen=(31, 119, 180))
        self.dr.setMinimum(minv)
        self.dr.setMaximum(maxv)
        self.dr.setValue(dr)
        self.dr_slider.setMinimum(minv)
        self.dr_slider.setMaximum(maxv)
        self.dr_slider.setValue(dr)
        self.ds.setMinimum(minv)
        self.ds.setMaximum(maxv)
        self.ds.setValue(ds)
        self.ds_slider.setMinimum(minv)
        self.ds_slider.setMaximum(maxv)
        self.ds_slider.setValue(ds)

 
    def update(self, dr=None, ds=None, xmin=None, xmax=None):
        if ds is None:
            ds = self.ds.value()
        if dr is None:
            dr = self.dr.value()
        if xmin is None:
            xmin = self.xmin.value()
        if xmax is None:
            xmax = self.xmax.value()
        y = calc_y(r, dr, xmin, xmax)
        self.curve1.setData(y)
        y = calc_y(s, ds, xmin, xmax)
        self.curve2.setData(y)
        t, n = calc_n(r, s, dr=dr, ds=ds, xmin=xmin, xmax=xmax)
        self.curve3.setData(n)

    @slot(int)
    def on_dr_valueChanged(self, dr):
        self.update(dr=dr)

    @slot(int)
    def on_ds_valueChanged(self, ds):
        self.update(ds=ds)

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
