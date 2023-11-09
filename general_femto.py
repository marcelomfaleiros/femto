# -*- coding: utf-8 -*-
# revisão 07/11/2023

import sys
import os
from general_femto_interface import Ui_QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets as qtw
import newport_smc100cc as smc100
import numpy as np
import time
import keyboard

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

        self.init_pos_lineEdit.setText("10")
        self.fin_pos_lineEdit.setText("200")
        self.step_lineEdit.setText("110")
                        
        self.init_pushButton.clicked.connect(self.initialization)
        #self.one_fs_pushButton.clicked.connect()
        #self.five_fs_pushButton.clicked.connect()
        #self.ten_fs_pushButton.clicked.connect()
        #self.twenty_fs_pushButton.clicked.connect()
        #self.set_zero_pushButton.clicked.connect()
        #self.move_to_pushButton.clicked.connect()
        self.start_pushButton.clicked.connect(self.measure)
        self.save_pushButton.clicked.connect(self.save)
        self.clear_pushButton.clicked.connect(self.clear)
        self.exit_pushButton.clicked.connect(self.exit)

    def graph_start_up(self):
        self.graphicsView.showGrid(x=True, y=True, alpha=True)
        self.graphicsView.setLabel("left", "deltaO", units="a.u.")
        self.graphicsView.setLabel("bottom", "Wavelength", units="nm")

        self.graphicsView.plot(TransientAbsorption.wl_array, TransientAbsorption.deltaO_array)

    def initialization(self):
        #initialize stage
        self.shutter = tl.ThorlabsSC10()                        #set up thorlabs shutter
        self.shutter.rs232_set_up('COM5')
        if self.shutter.id() == 'THORLABS SC10 VERSION 1.07':
            self.initialize_label.setText("Homed: position = " + str(initialize_pos)
                                          + '\nTHORLABS SC10 VERSION 1.07 - OK')
        #initialize lock-in amplifier
        
        self.graph_start_up()

    def zero_delay(self):        
        #self.zero = self.stage.status["position"]
        self.zero_pos_mm = self.zero/20000
        self.set_zero_delay_label.setText("Zero delay = " + str(self.zero_pos_mm) + " mm")
        return self.zero      

    def move_stage_rel(self, step_fs):
        pass 

    def move_stage_mm(self):
        pass

    def move_stage_fs(self, position_fs):
        pass

    def intensity(self):    
        pass

    def alignment(self, integ_time):
        pass      

    def measure(self):
        pass

    def save(self, mode=str):
        if mode == 'transient_spectrum':
            raw_ta_array = np.vstack(TransientAbsorption.ta_array)
            ta_data = raw_ta_array.transpose()
            file_spec = qtw.QFileDialog.getSaveFileName()[0]
            np.savetxt(file_spec, ta_data, header=self.delay_string[1:-1])  #fmt='%1.2f',
        elif mode == 'dynamics':
            raw_ta_array = np.vstack(TransientAbsorption.dynamics_array)                      
            ta_data = raw_ta_array.transpose()
            file_spec = qtw.QFileDialog.getSaveFileName()[0]
            np.savetxt(file_spec, ta_data)                                  #, fmt='%1.2f'

    def clear(self):
        self.graphicsView.clear()

    def exit(self):       
        self.close()

if __name__ == '__main__':
    app = qtw.QApplication([])
    tela = GeneralFemto()
    tela.show()
    app.exec_()