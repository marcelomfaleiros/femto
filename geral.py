# -*- coding: utf-8 -*-
# revisão 07/11/2023

import sys
import os
#from transient_absorption_interface_v3 import Ui_MainWindow
#from ta_dynamics_interface import Ui_Form
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets as qtw
import newport_smc100cc as smc100
#import thorlabs_sc10 as tl
import numpy as np
import time
import keyboard

class TransientAbsorption(qtw.QMainWindow, Ui_MainWindow):
    '''
    
    Usage
    -----
    import transient_absorption as ta
    import time

    '''

    ta_array = []
    wl_array = []
    delay_array = []
    dynamics_array = []
    deltaO_array = []
           
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName("Transient Absorption")
        self.setupUi(self)

        self.strt_inttime_lineEdit.setText("10")
        self.strt_delay_lineEdit.setText("200")
        self.arb_move_lineEdit.setText("110")
        self.spc_delay_lineEdit.setText("0")
        self.spc_inttime_lineEdit.setText("10")
        self.dyn_inidelay_lineEdit.setText("-10000")
        self.dyn_findelay_lineEdit.setText("50000")
        self.dyn_stpdelay_lineEdit.setText("10000")
        self.dyn_inttime_lineEdit.setText("10")
                
        self.initialize_pushButton.clicked.connect(self.initialization)
        self.set_zerodelay_pushButton.clicked.connect(self.zero_delay)
        self.align_pushButton.clicked.connect(self.alignment)
        self.align_exit_pushButton.clicked.connect(self.exit)
        self.arb_move_pushButton.clicked.connect(self.move_stage_mm)
        self.one_fs_pushButton.clicked.connect(lambda: self.move_stage_rel(1))
        self.none_fs_pushButton.clicked.connect(lambda: self.move_stage_rel(-1))
        self.five_fs_pushButton.clicked.connect(lambda: self.move_stage_rel(5))
        self.nfive_fs_pushButton.clicked.connect(lambda: self.move_stage_rel(-5))
        self.ten_fs_pushButton.clicked.connect(lambda: self.move_stage_rel(10))
        self.nten_fs_pushButton.clicked.connect(lambda: self.move_stage_rel(-10))        
        self.spc_meas_pushButton.clicked.connect(lambda: self.ta_dynamics(True))
        self.spc_clean_pushButton.clicked.connect(self.clear)
        self.spc_save_pushButton.clicked.connect(self.save)
        self.spc_exit_pushButton.clicked.connect(self.exit)
        self.dyn_meas_pushButton.clicked.connect(lambda: self.ta_dynamics(False))
        self.dyn_pushButton.clicked.connect(self.open_ta_window)
        self.dyn_clean_pushButton.clicked.connect(self.clear)
        self.dyn_save_pushButton.clicked.connect(lambda: self.save('transient_spectrum'))
        self.dyn_exit_pushButton.clicked.connect(self.exit)

    def open_ta_window(self):
        self.ta_window = qtw.QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi_interface(self.ta_window)   
        self.ta_window.show()
              
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

    def open_ta_window(self):
        self.ta_window = DynamicsWindow(self)
        self.ta_window.show()

class DynamicsWindow(qtw.QWidget, Ui_Form):
    def __init__(self, TransientAbsorption):
        super().__init__()
        self.setObjectName("Dynamics")
        self.setupUi(self)

        self.graph_start_up()

        [self.ta_dyn_comboBox.addItem(str(i)) for i in TransientAbsorption.wl_array]    #charge comboBox with wavelengths

        self.ta_dyn_comboBox.activated[str].connect(self.choose_delay)
        
        self.ta_dyn_clean_pushButton.clicked.connect(self.clear)
        self.ta_dyn_save_pushButton.clicked.connect(lambda: TransientAbsorption.save('dynamics'))
        self.ta_dyn_exit_pushButton.clicked.connect(self.exit)

    def graph_start_up(self):
        self.intensity_array = []       #define the left empty array

        self.ta_dyn_graphicsView.showGrid(x=True, y=True, alpha=True)       #define plot grid
        self.ta_dyn_graphicsView.setLabel("left", "deltaO", units="a.u.")   #define left plot label
        self.ta_dyn_graphicsView.setLabel("bottom", "Delay", units="ps")    #define bottom plot label

        self.ta_dyn_graphicsView.plot(TransientAbsorption.delay_array, self.intensity_array)   #plot an empty data array

    def choose_delay(self, wl_text):
        wl = float(wl_text)
        index_wl = np.where(TransientAbsorption.ta_array == wl)[1]
        ta_intensity_array = np.delete(TransientAbsorption.ta_array, 0, 0)
        ta_intensity_array_transp = ta_intensity_array.transpose()     
        self.intensity_array = ta_intensity_array_transp[index_wl - 1].ravel()
        self.ta_dyn_graphicsView.plot(TransientAbsorption.delay_array, self.intensity_array, pen =(0, 114, 189), symbolPen ='w',
                                      symbol='o', symbolSize=3, clear=False)
        TransientAbsorption.dynamics_array = np.array([TransientAbsorption.delay_array, self.intensity_array])

    def clear(self):
        self.ta_dyn_graphicsView.clear()

    def exit(self):
        self.close()

if __name__ == '__main__':
    app = qtw.QApplication([])
    tela = TransientAbsorption()
    tela.show()
    app.exec_()
