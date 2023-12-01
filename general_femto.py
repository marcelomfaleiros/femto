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

        intensity_array = np.array([0])
        delay_array = np.array([0])
              
        for d in range(self.init_pos, (self.fin_pos + self.step), self.step):
            if keyboard.is_pressed('Escape'):
                break 
            delay_array = np.append(delay_array, d)  
            self.move_stage_fs(d)          
            #lock-in
            y = self.sr830.measure_buffer(channel, self.sampling_time)
            #intensity_array.append(lock-in measurement)
            intensity_array = np.append(intensity_array, y)
            self.point = (delay_array, intensity_array)
             
            self.signal.emit(self.point)

        self.data = intensity_array, delay_array

        self.finished.emit()

class GeneralFemto(qtw.QMainWindow, Ui_QMainWindow):
    '''

    Usage
    -----
    import general_femto as gf
    from time import sleep

    '''
           
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName("General Femto")
        self.setupUi(self)

        self.thread = Worker()

        self.init_pos_lineEdit.setText("-100")
        self.fin_pos_lineEdit.setText("200")
        self.step_lineEdit.setText("10")
        self.move_to_lineEdit.setText("0")
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
        self.delay_pushButton.clicked.connect(self.move_stage_fs)
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
        self.thread.smc.initialize()
        #initialize lock-in amplifier
        self.thread.sr830 = srs.LIA_SR830()
        self.thread.sr830.initialize()
        #initialize graph
        self.graph_start_up()

    def zero_delay(self):        
        self.zero = self.thread.smc.current_position()                      #read current stage position
        self.zero_delay_label.setText("Zero delay (mm): " + str(self.zero))
        return self.zero      

    def move_stage_rel(self, step_fs):
        self.thread.smc.move_rel_fs(step_fs) 
        current_mm = self.thread.smc.current_position()                     #read current stage position
        self.current_mm_label.setText("Current (mm): " + str(current_mm))   #display current position in mm

    def move_stage_mm(self):
        target_position_mm = float(self.move_to_lineEdit.text())            #read target position from interface
        self.thread.smc.move_abs_mm(target_position_mm)                     #move to target position in mm
        current_mm = self.thread.smc.current_position()                     #read current stage position
        self.current_mm_label.setText("Current (mm): " + str(current_mm))   #display current position in mm

    def move_stage_fs(self):
        target_delay = float(self.delay_lineEdit.text())                            #read target position from interface
        target_fs = target_delay + self.zero/0.0003                                 #compute target delay position
        self.thread.smc.move_abs_fs(target_fs)                                      #move to target position in fs
        current_mm = self.thread.smc.current_position()                             #read current stage position
        self.current_mm_label.setText("Current (mm): " + str(current_mm))           #display current position in mm
        current_fs = (current_mm - self.zero)/0.0003                       #convert to fs
        self.current_fs_label.setText("Current (fs): " + str(round(current_fs, 1))) #display current position in mm

    def intensity(self):
        x = 0
        y = 0
        x_array = []
        y_array = []
        while True:
            if keyboard.is_pressed('Escape'):
                break
            y = self.thread.sr830.measure_display(1000)
            y_array.append(y)
            x_array.append(x)
            point = (x_array, y_array)
            self.plot(point)
            x += 1

    def measure(self):
        self.thread.channel = self.comboBox.currentText()
        self.thread.move_to = int(self.intTime_lineEdit.text()) * 1000
        self.thread.delay = int(self.delay_lineEdit.text())
        self.thread.init_pos = float(self.init_pos_lineEdit.text())
        self.thread.fin_pos = float(self.fin_pos_lineEdit.text())
        self.thread.step = float(self.step_lineEdit.text())
        self.thread.sampling_time = float(self.sample.lineEdit.text())
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
        self.thread.smc.rs232_close()   
        self.close()

if __name__ == '__main__':
    app = qtw.QApplication([])
    tela = GeneralFemto()
    tela.show()
    app.exec_()