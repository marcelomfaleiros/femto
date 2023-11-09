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

        self.init_pos_lineEdit.setText("-100")
        self.fin_pos_lineEdit.setText("200")
        self.step_lineEdit.setText("10")
        self.move_to_lineEdit.setText("100")
                        
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
        self.graphicsView.setLabel("left", "deltaO", units="a.u.")
        self.graphicsView.setLabel("bottom", "Wavelength", units="nm")

        self.graphicsView.plot(TransientAbsorption.wl_array, TransientAbsorption.deltaO_array)

    def initialization(self):
        #initialize stage
        smc = smc100.SMC100CC()
        smc.rs232_set_up()

        #initialize lock-in amplifier
        
        self.graph_start_up()

    def zero_delay(self):        
        self.zero = self.smc.current_position()
        #self.zero_pos_mm = self.zero/20000
        #self.set_zero_delay_label.setText("Zero delay = " + str(self.zero_pos_mm) + " mm")
        return self.zero      

    def move_stage_rel(self, step_fs):
        self.smc.move_rel_fs(step_fs) 

    def move_stage_mm(self):
        #read position from interface
        target_position_mm = float(self.move_to_lineEdit.text())
        self.smc.move_abs_mm(target_position_mm)

    def move_stage_fs(self, position_fs):
        pass

    def intensity(self):  
        #point from lock-in amplifier  
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