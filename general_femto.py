# -*- coding: utf-8 -*-

""" 
    Author: Marcelo Meira Faleiros
    State University of Campinas, Brazil

"""

import sys
import os
from general_femto_interface import Ui_QMainWindow
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QComboBox
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets as qtw
import srs_sr830 as srs
import newport_smc100cc as smc100
import numpy as np
from time import sleep
import keyboard

class Worker(QThread):
    signal = pyqtSignal(object)
    finished = pyqtSignal()
    
    def run(self, mode = str):
        if self.channel == 'CH1 output':
            channel = 'ch1'
        elif self.channel == 'CH2 output':
            channel = 'ch2'

        intensity_array = []
        
        t_array = [round(i * self.tstep, 2) for i in range(self.n_spectra + 1)]
        t_array = np.array(t_array)
        self.t_string = np.array2string(t_array, precision=2, separator=' ', suppress_small=True)
        
        for i in t_array:
            if keyboard.is_pressed('Escape'):
                break             
            #lock-in
            y = self.sr830.measure(channel, 1)
            self.point = (t_array[i], y)
            #intensity_array.append(lock-in measurement) 
            intensity_array.append(y)

            self.signal.emit(self.point)

            sleep(self.tstep)

        intensity_array = np.array(intensity_array)
        self.data = intensity_array, t_array

        self.finished.emit()

class GeneralFemto(qtw.QMainWindow, Ui_QMainWindow):
    '''

    Usage
    -----
    import general_femto as gf
    import time

    '''
           
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName("General Femto")
        self.setupUi(self)

        self.thread = Worker()

        self.init_pos_lineEdit.setText("-100")
        self.fin_pos_lineEdit.setText("200")
        self.step_lineEdit.setText("10")
        self.move_to_lineEdit.setText("100")
        self.delay_lineEdit.setText("0")

        self.comboBox.addItems(['CH1 output','CH2 output'])
                        
        self.init_pushButton.clicked.connect(self.initialization)
        self.freerun_pushButton.clicked.connect(self.intensity)
        self.one_fs_pushButton.clicked.connect(lambda: self.move_stage_rel(1))
        self.mone_fs_pushButton.clicked.connect(lambda: self.move_stage_rel(-1))
        self.five_fs_pushButton.clicked.connect(lambda: self.move_stage_rel(5))
        self.mfive_fs_pushButton.clicked.connect(lambda: self.move_stage_rel(-5))
        self.ten_fs_pushButton.clicked.connect(lambda: self.move_stage_rel(10))
        self.mten_fs_pushButton.clicked.connect(lambda: self.move_stage_rel(-10))
        self.twenty_fs_pushButton.clicked.connect(lambda: self.move_stage_rel(20))
        self.mtwenty_fs_pushButton.clicked.connect(lambda: self.move_stage_rel(-20))
        self.set_zero_pushButton.clicked.connect(self.zero_delay)
        self.move_to_pushButton.clicked.connect(self.move_stage_mm)
        self.start_pushButton.clicked.connect(self.measure)
        self.save_pushButton.clicked.connect(self.save)
        self.clear_pushButton.clicked.connect(self.clear)
        self.exit_pushButton.clicked.connect(self.exit)

    def graph_start_up(self):
        self.graphicsView.showGrid(x=True, y=True, alpha=True)
        self.graphicsView.setLabel("left", "Intensity", units="a.u.")
        self.graphicsView.setLabel("bottom", "Delay", units="fs")

    def initialization(self):
        #initialize stage
        self.thread.smc = smc100.SMC100CC()
        self.thread.smc.rs232_set_up()
        #initialize lock-in amplifier
        self.thread.sr830 = srs.LIA_SR830()
        self.thread.sr830.gpib_set_up()
        self.thread.sr830.initialize()
        #initialize graph
        self.graph_start_up()

    def zero_delay(self):        
        self.zero = self.smc.current_position()  #read current stage position
        #self.zero_pos_mm = self.zero/20000      #convert stage position into mm
        #self.set_zero_delay_label.setText("Zero delay = " + str(self.zero_pos_mm) + " mm")
        return self.zero      

    def move_stage_rel(self, step_fs):
        self.thread.smc.move_rel_fs(step_fs) 

    def move_stage_mm(self):
        #read position from interface
        target_position_mm = float(self.move_to_lineEdit.text())
        self.thread.smc.move_abs_mm(target_position_mm)

    def move_stage_fs(self, position_fs):
        target_position_fs = float(self.delay_lineEdit.text())
        self.thread.smc.move_abs_mm(target_position_fs)

    def intensity(self):
        x = 0
        while True:
            y = self.sr830.measure(1)
            x += 1
            point(x, y)
            self.plot(point)
            sleep(1)

    def measure(self):
        self.thread.channel = self.comboBox.currentText()
        self.thread.move_to = int(self.intTime_lineEdit.text()) * 1000
        self.thread.delay = int(self.delay_lineEdit.text())
        self.thread.init_pos = float(self.init_pos_lineEdit.text())
        self.thread.fin_pos = float(self.fin_pos_lineEdit.text())
        self.thread.step = float(self.step_lineEdit.text())
        self.thread.signal.connect(self.plot)
        self.thread.start()

        self.init_pushButton.setEnabled(False)
        self.one_fs_pushButton.setEnabled(False)
        self.mone_fs_pushButton.setEnabled(False)
        self.five_fs_pushButton.setEnabled(False)
        self.mfive_fs_pushButton.setEnabled(False)
        self.ten_fs_pushButton.setEnabled(False)
        self.mten_fs_pushButton.setEnabled(False)
        self.twenty_fs_pushButton.setEnabled(False)
        self.mtwenty_fs_pushButton.setEnabled(False)
        self.move_to_pushButton.setEnabled(False)
        self.delay_pushButton.setEnabled(False)
        self.freerun_pushButton.setEnabled(False)
        self.start_pushButton.setEnabled(False)
        self.save_pushButton.setEnabled(False)
        self.clear_pushButton.setEnabled(False)
        self.exit_pushButton.setEnabled(False)
        self.thread.finished.connect(lambda: self.start_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.freeRun_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.save_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.clear_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.exit_pushButton.setEnabled(True))

    def plot(self, point):
        self.graphicsView.plot(point[0], point[1], clear=False)
        pg.QtWidgets.QApplication.processEvents()

    def save(self, mode=str):
        raw_data = self.thread.data.transpose()
        transposed_raw_data = np.vstack(raw_data)                      
        data = transposed_raw_data.transpose()
        file_spec = qtw.QFileDialog.getSaveFileName()[0]
        np.savetxt(file_spec, data)    

    def clear(self):
        self.graphicsView.clear()

    def exit(self):       
        self.close()

if __name__ == '__main__':
    app = qtw.QApplication([])
    tela = GeneralFemto()
    tela.show()
    app.exec_()