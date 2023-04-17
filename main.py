import sys
from math import pi     
 
import numpy as np                                               
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
r = df1.scan; s = df2.scan

def calc_y(r, v=-141, xmin=170, xmax=190):
    return np.unwrap(np.angle(np.fft.fft(np.roll(r, v))))[xmin:xmax]#-v*np.linspace(0, 2*pi, len(r))

class ExampleApp(QtWidgets.QMainWindow, Design):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Этот метод из класса Design, он инициализирует виджеты
        self.x = np.arange(len(r))
        minv, maxv, v = -200, 0, -141
        y = calc_y(r)
        self.curve = self.canvas.plot(y, pen=(31, 119, 180))
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
        self.curve.setData(y)

    @slot(int)
    def on_v_valueChanged(self, v):
        self.update(v)

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))   # Более современная тема оформления
    app.setPalette(QtWidgets.QApplication.style().standardPalette())  # Берём цвета из темы оформления
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
