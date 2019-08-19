import tkinter as tk
import numpy as np
import cv2
from PIL import ImageGrab
from PyQt5 import QtWidgets, QtCore, QtGui
import SnippingMenu
from PyQt5.QtCore import Qt
import ctypes
from pyrobot import Robot


robot = Robot()


class SnippingWidget(QtWidgets.QWidget):
    num_snip = 0
    is_snipping = False
    background = True

    def __init__(self, parent=None, x=0, y=0):
        super(SnippingWidget, self).__init__()
        self.parent = parent
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        size = (ctypes.windll.user32.GetSystemMetrics(78), ctypes.windll.user32.GetSystemMetrics(79))

        root = tk.Tk()
        
        self.x = x
        self.y = y
        self.width = size[0]
        self.height = size[1]

        self.setGeometry(self.x, self.y, self.width, self.height)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()

    def start(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        SnippingWidget.background = False
        SnippingWidget.is_snipping = True
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        print('Capture the screen...')
        print('Press q if you want to quit...')
        self.show()

    def paintEvent(self, event):
        if SnippingWidget.is_snipping:
            brush_color = (128, 128, 255, 100)
            lw = 3
            opacity = 0.3
        else:
            # reset points, so the rectangle won't show up again.
            self.begin = QtCore.QPoint()
            self.end = QtCore.QPoint()
            brush_color = (0, 0, 0, 0)
            lw = 0
            opacity = 0

        self.setWindowOpacity(opacity)
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), lw))
        qp.setBrush(QtGui.QColor(*brush_color))
        rect = QtCore.QRectF(self.begin, self.end)
        qp.drawRect(rect)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Q:
            print('Quit')
            self.close()
        event.accept()

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.globalBegin = event.globalPos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.globalEnd = event.globalPos()
        self.update()

    def mouseReleaseEvent(self, event):
        SnippingWidget.num_snip += 1
        SnippingWidget.is_snipping = False
        QtWidgets.QApplication.restoreOverrideCursor()

        x1 = min(self.globalBegin.x(), self.globalEnd.x())
        y1 = min(self.globalBegin.y(), self.globalEnd.y())
        x2 = max(self.globalBegin.x(), self.globalEnd.x())
        y2 = max(self.globalBegin.y(), self.globalEnd.y())

        self.repaint()
        QtWidgets.QApplication.processEvents()

        coords = (x1, y1, x2, y2)
        img = robot.take_screenshot(coords)

        QtWidgets.QApplication.processEvents()
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

        # add to the snips list the object that opens a window of the image
        SnippingMenu.Menu(img, SnippingWidget.num_snip, (x1, y1, x2, y2))