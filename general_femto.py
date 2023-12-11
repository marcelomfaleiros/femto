# -*- coding: utf-8 -*-

""" 
    Author: Marcelo Meira Faleiros
    State University of Campinas, Brazil
"""

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
    position_mm = pyqtSignal(float)

    def move_stage_fs(self, target_delay):                                     
        target_fs = target_delay + self.zero/0.0003             #compute target delay position
        self.smc.move_abs_fs(target_fs)                         #move to target position in fs
        self.current_mm = self.smc.current_position()           #read current stage position          
        self.position_mm.emit(self.current_mm)

    def run(self, mode = str):
        if self.channel == 'CH1 output':
            channel = 'ch1'
        elif self.channel == 'CH2 output':
            channel = 'ch2'

        intnsity_array = []
        dlay_array = []
              
        for target_delay in range(self.init_pos, (self.fin_pos + self.step), self.step):
            if keyboard.is_pressed('Escape'):
                break 
            dlay_array.append(target_delay)  
            self.move_stage_fs(target_delay)        
            #lock-in
            y = self.sr830.measure_buffer(self.sampling_time)
            #intensity_array.append(lock-in measurement)
            intnsity_array.append(y)

            delay_array = np.array(dlay_array)
            intensity_array = np.array(intnsity_array)
            self.point = (delay_array, intensity_array)
             
            self.signal.emit(self.point)

        self.data = delay_array, intensity_array
        self.mode = 'measure'
    
        self.finished.emit()

class GeneralFemto(qtw.QMainWindow, Ui_QMainWindow):
    '''

    
    '''           
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName("General Femto")
        self.setupUi(self)

        self.is_zero_defined = False

        self.thread = Worker()
        #initializing line edit fields
        self.init_pos_lineEdit.setText("-5000")
        self.fin_pos_lineEdit.setText("20000")
        self.step_lineEdit.setText("5000")
        self.move_to_lineEdit.setText("0")
        self.delay_lineEdit.setText("0")
        self.sample_lineEdit.setText("1")

        self.comboBox.addItems(['CH1 output','CH2 output'])
        #defining action for the buttons
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
        self.delay_pushButton.clicked.connect(lambda: self.move_stage_fs(float(self.delay_lineEdit.text())))
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
        self.thread.zero = self.zero
        self.zero_delay_label.setText("Zero delay (mm): " + str(self.zero)) #display zero delay position
        self.current_fs_label.setText("Current (fs): 0")                  #display zero delay position
        self.is_zero_defined = True
        return self.zero      

    def move_stage_rel(self, step_fs):
        self.thread.smc.move_rel_fs(step_fs)                                #move one step
        current_mm = self.thread.smc.current_position()                     #read current stage position

    def move_stage_mm(self):
        target_position_mm = float(self.move_to_lineEdit.text())            #read target position from interface
        self.thread.smc.move_abs_mm(target_position_mm)                     #move to target position in mm
        current_mm = self.thread.smc.current_position()                     #read current stage position
        self.show_position(current_mm) 

    def move_stage_fs(self, target_delay):                                     
        target_fs = target_delay + self.zero/0.0003                         #compute target delay position
        self.thread.smc.move_abs_fs(target_fs)
        current_mm = self.thread.smc.current_position()                     #read current stage position
        self.show_position(current_mm)
        
    def show_position(self, current_mm):                                    #move to target position in fs
        self.current_mm_label.setText("Current (mm): " + str(current_mm))   #display current position in mm
        if self.is_zero_defined ==  True:
            current_fs = (current_mm - self.zero)/0.0003 
            self.current_fs_label.setText("Current (fs): " + str(round(current_fs, 1))) #display current position in mm
        elif self.is_zero_defined ==  False:
            self.zero_delay_label.setText("Zero delay (mm): Not defined")   #display zero delay position
            self.current_fs_label.setText("Current (fs): Not defined")      #display current position in mm

    def intensity(self):
        x = 0
        y = 0
        x_array = []
        y_array = []
        while True:
            if keyboard.is_pressed('Escape'):
                break
            y = self.thread.sr830.measure_display(20)
            y_array.append(y)
            x_array.append(x)
            point = (x_array, y_array)
            self.plot(point)
            x += 1
        self.data = point
        self.thread.mode = 'free run'

    def measure(self):
        #set interface elements as Worker thread elements
        self.thread.channel = self.comboBox.currentText()
        self.thread.move_to = float(self.move_to_lineEdit.text())
        self.thread.delay = int(self.delay_lineEdit.text())
        self.thread.init_pos = int(self.init_pos_lineEdit.text())
        self.thread.fin_pos = int(self.fin_pos_lineEdit.text())
        self.thread.step = int(self.step_lineEdit.text())
        self.thread.sampling_time = float(self.sample_lineEdit.text())
        self.thread.signal.connect(self.plot)
        self.thread.position_mm.connect(self.show_position)
        self.thread.start()
        #disable interface buttons while measurement is running
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
        self.exit_pushButton.setEnabled(True)
        #connect the interface buttons to the Worker thread
        self.thread.finished.connect(lambda: self.init_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.one_fs_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.mone_fs_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.five_fs_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.mfive_fs_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.ten_fs_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.mten_fs_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.twenty_fs_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.mtwenty_fs_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.move_to_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.delay_pushButton.setEnabled(True))        
        self.thread.finished.connect(lambda: self.start_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.freerun_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.save_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.clear_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.exit_pushButton.setEnabled(True))

    def plot(self, point):
        self.graphicsView.plot(point[0], point[1], pen=None, symbol='o', clear=False)
        pg.QtWidgets.QApplication.processEvents()

    def save(self):  
        if self.thread.mode == 'measure':
            raw_data = np.array(self.thread.data)
        elif self.thread.mode == 'free run':
            raw_data = np.array(self.data)
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