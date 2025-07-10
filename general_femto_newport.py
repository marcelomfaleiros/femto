# -*- coding: utf-8 -*-
"""Optical experiment interface with Newport stage and SR830 lock-in control.

Provides:
- PyQt5 GUI control
- Automated fs-range scanning - Newport SMC100CC translation stage control
- Synchronized data acquisition - SR830 lock-in amplifier
- Real-time pyqtgraph visualization

Author: Marcelo Meira Faleiros
Laboratory: State University of Campinas, Brazil
Last modified: 2025-07-10
"""

from general_femto_interface import Ui_QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets as qtw
import srs_sr830 as srs
import newport_smc100cc as smc100
import numpy as np
import keyboard

# Constantes de conversão
FS_TO_MM_FACTOR = 0.0003  # Fator de conversão femtossegundos → milímetros

class Worker(QThread):
    """Thread for asynchronous stage control and data acquisition operations.

    Attributes:
        signal (pyqtSignal): Signal emitted for real-time data updates.
        finished (pyqtSignal): Signal emitted when execution completes.
        position_mm (pyqtSignal): Signal carrying current stage position (in mm).
    """
    
    signal = pyqtSignal(object)
    finished = pyqtSignal()
    position_mm = pyqtSignal(float)

    def move_stage_fs(self, target_delay):     
        """Move o estágio para uma posição específica baseada em atraso em femtossegundos.

        Args:
            target_delay (float): Atraso desejado em femtossegundos (fs).
        """ 
        target_fs = target_delay + self.zero/FS_TO_MM_FACTOR             
        self.smc.move_abs_fs(target_fs)                         
        self.current_mm = self.smc.current_position()                     
        self.position_mm.emit(self.current_mm)

    def run(self):
        """Executa a medição com base no passo em fs e no tempo de aquisição.""" 
        self.mode = 'measure'
        channel = 'ch1' if self.channel == 'CH1 output' else 'ch2'
        intnsity_array = []
        dlay_array = []
              
        for target_delay in range(self.init_pos, (self.fin_pos + self.step), self.step):
            if keyboard.is_pressed('Escape'):
                break 
            dlay_array.append(target_delay)  
            self.move_stage_fs(target_delay)        
            y = self.sr830.measure_buffer(channel, self.sampling_time)
            #intensity_array.append(lock-in measurement)
            intnsity_array.append(y)

            delay_array = np.array(dlay_array)
            intensity_array = np.array(intnsity_array)
            self.point = (delay_array, intensity_array)
             
            self.signal.emit(self.point)

        self.data = delay_array, intensity_array
    
        self.finished.emit()

class GeneralFemto(qtw.QMainWindow, Ui_QMainWindow):
    """Main interface for control of femtoseconds experiments.""" 

    def __init__(self, *args, **kwargs):
        """Initialize the femtosecond experiment control interface.

        Sets up the main application window, UI components, and initial state variables.
        Configures signal-slot connections for all interactive elements.

        Args:
            *args: Variable length argument list passed to QMainWindow.
            **kwargs: Arbitrary keyword arguments passed to QMainWindow.

        Attributes initialized:
            is_zero_defined (bool): Flag indicating if stage zero position is calibrated.
            thread (Worker): Background worker thread for hardware control.
        
        UI Initializations:
            - Sets default values for all input fields
            - Configures measurement channel options
            - Connects all button click handlers
        """
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
        """Initialize and configure the real-time data visualization plot.
    
        Sets up the pyqtgraph plot widget with:
        - Grid lines (both x and y axes)
        - Axis labels with units
        - Default styling for experimental data visualization

        Configures:
        x-axis: "Delay" (units: fs)
        y-axis: "Intensity" (units: a.u.)
        Grid: Enabled with 50% opacity

        Note:
        This should be called once during application initialization,
        before any plotting operations begin.
        """
        self.graphicsView.showGrid(x=True, y=True, alpha=True)
        self.graphicsView.setLabel("left", "Intensity", units="a.u.")
        self.graphicsView.setLabel("bottom", "Delay", units="fs")

    def initialization(self):
        """Initialize the stage and the lock-in amplifier."""
        try:
            self.thread.smc = smc100.SMC100CC()
            self.thread.smc.initialize()
            self.thread.sr830 = srs.LIA_SR830()
            self.thread.sr830.initialize()
            self.graph_start_up()
        except Exception as e:
            qtw.QMessageBox.critical(self, "Erro de Hardware", 
                                    f"Falha na inicialização:\n{str(e)}")

    def zero_delay(self):       
        """Set the current position as zero delay position.""" 
        self.zero = self.thread.smc.current_position()                      
        self.thread.zero = self.zero
        self.zero_delay_label.setText("Zero delay (mm): " + str(self.zero)) #display zero delay position
        self.current_fs_label.setText("Current (fs): 0")                    #display zero delay position
        self.is_zero_defined = True
        return self.zero

    def move_stage_mm(self):
        """Move stage to a position specified in milimeters (mm)."""
        target_position_mm = float(self.move_to_lineEdit.text())           
        self.thread.smc.move_abs_mm(target_position_mm)                     
        current_mm = self.thread.smc.current_position()                     
        self.show_position(current_mm) 

    def move_stage_fs(self, target_delay):    
        """Move stage to a position specified in femtoseconds (fs)."""
        target_fs = target_delay + self.zero/FS_TO_MM_FACTOR                         
        self.thread.smc.move_abs_fs(target_fs)
        current_mm = self.thread.smc.current_position()                     
        self.show_position(current_mm)
    
    def move_stage_rel(self, step):     
        """Move the stage by a relative distance in femtoseconds.

        Args:
        step (float): Relative movement distance in femtoseconds (fs). 
                      Positive values move forward, negative values move backward.

        Note:
        - Updates the displayed position automatically
        - Uses the stage's native femtosecond movement resolution
        - Blocks until movement completes

        Example:
        >>> move_stage_rel(500)   # Move forward 500 fs
        >>> move_stage_rel(-1000) # Move backward 1000 fs   
        """
        self.thread.smc.move_rel_fs(step)
        current_mm = self.thread.smc.current_position()                     
        self.show_position(current_mm)

    def show_position(self, current_mm):                                    
        """Display the current position in real time."""
        self.current_mm_label.setText("Current (mm): " + str(current_mm))   #display current position in mm
        if self.is_zero_defined ==  True:
            current_fs = (current_mm - self.zero)/FS_TO_MM_FACTOR
            self.current_fs_label.setText("Current (fs): " + str(round(current_fs, 1))) #display current position in mm
        elif self.is_zero_defined ==  False:
            self.zero_delay_label.setText("Zero delay (mm): Not defined")   #display zero delay position
            self.current_fs_label.setText("Current (fs): Not defined")      #display current position in mm

    def intensity(self):
        """Perform continuous intensity measurements in free-run mode.

        Continuously acquires data from the lock-in amplifier (channel 1) until 
        the Escape key is pressed. Displays real-time measurements in the plot.

        Operation:
        1. Enters 'free run' measurement mode
        2. Continuously measures intensity at fixed time intervals
        3. Updates the plot in real-time
        4. Stores acquired data in `self.data` when stopped

        Data Structure:
        The collected data is stored as a tuple of numpy arrays:
        - point[0]: Sample indices (0, 1, 2, ...)
        - point[1]: Intensity values (in a.u.)

        Note:
        Press ESC key to stop the measurement.
        Uses a fixed 10ms sampling time for each measurement.

        Side Effects:
        - Updates `self.mode` to 'free run'
        - Modifies `self.data` with collected measurements
        - Continuously updates the GUI plot
        """
        self.thread.mode = 'free run'
        x = 0
        y = 0
        x_array = []
        y_array = []
        while True:
            if keyboard.is_pressed('Escape'):
                break
            y = self.thread.sr830.measure_display('ch1', 10)
            y_array.append(y)
            x_array.append(x)
            point = (x_array, y_array)
            self.plot(point)
            x += 1
        self.data = point

    def measure(self):
        """Execute an automated delay scan measurement sequence.

        Coordinates a complete measurement cycle:
        1. Configures scan parameters from UI inputs
        2. Initializes data acquisition
        3. Performs synchronized stage movement and lock-in measurements
        4. Handles real-time data visualization
        5. Manages UI state during operation

        Workflow:
        - Reads start/stop/step values from UI fields
        - Configures worker thread with measurement parameters
        - Disables UI controls during measurement
        - Enables progress monitoring via signals
        - Automatically re-enables UI when complete

        Signals:
        - thread.signal: Emits (delay_array, intensity_array) tuples
        - thread.finished: Indicates measurement completion

        UI Interactions:
        - Disables all control buttons during measurement
        - Only keeps Exit button active
        - Auto-restores UI when finished

        Notes:
        Measurement can be aborted via Escape key
        Uses sampling time specified in UI (default: 1s)
        Results stored in thread.data as (delays, intensities)

        Side Effects:
        - Modifies thread attributes (init_pos, fin_pos, etc.)
        - Alters enabled state of all UI controls
        - Updates plot widget in real-time
        """
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
        """Update the plot widget with new data points in real-time.

        Args:
        point (Tuple[np.ndarray, np.ndarray]): Data to plot, where:
            - point[0]: Array of delay values (x-axis) in femtoseconds
            - point[1]: Array of intensity values (y-axis) in arbitrary units

        Displays:
        - Points are plotted as circular markers ('o') without connecting lines
        - Maintains existing plot elements (non-destructive update)
        - Auto-scales axes to fit new data

        Note:
        - Uses pyqtgraph for high-performance plotting
        - Processes Qt events immediately for real-time display
        - Clears previous plot if `clear=False` is passed
        """
        self.graphicsView.plot(point[0], point[1], pen=None, symbol='o', clear=False)
        pg.QtWidgets.QApplication.processEvents()

    def save(self):  
        """Save measurement data to a text file.

        Handles data from both measurement modes:
        - 'measure' mode: Saves delay scan data (delay_array, intensity_array)
        - 'free run' mode: Saves time series data (sample_index, intensity_array)

        File Format:
        Two-column ASCII text file with headers:
        Column 1: Delay (fs) or Sample Index
        Column 2: Intensity (a.u.)

        Workflow:
        1. Opens file dialog for destination selection
        2. Transposes raw data for proper columnar format
        3. Saves with numpy.savetxt() using default formatting
        4. Preserves original data structure in memory

        UI Interaction:
        - Uses native file dialog (QFileDialog)
        - No UI state changes during operation

        Notes:
        - File format is platform-independent
        - Overwrites existing files without warning
        - Uses scientific notation for numeric values
        - Default file extension: .txt
        """
        if self.thread.mode == 'measure':
            raw_data = np.array(self.thread.data)
        elif self.thread.mode == 'free run':
            raw_data = np.array(self.data)
        transposed_raw_data = np.vstack(raw_data)                      
        data = transposed_raw_data.transpose()
        file_spec = qtw.QFileDialog.getSaveFileName()[0]
        np.savetxt(file_spec, data)    

    def clear(self):
        """Clear all data from the plotting widget.

        Resets the visualization display while preserving:
        - Current axis labels and units
        - Grid visibility settings
        - Plot styling configurations

        Note:
        - Does not affect stored data in memory (`self.data` or `self.thread.data`)
        - Maintains all plot properties (labels, grid, etc.)
        - Immediate visual update (no need to refresh UI)

        Side Effects:
        - Empties the pyqtgraph graphics view
        - Does not modify measurement parameters or hardware state
        """
        self.graphicsView.clear()

    def exit(self):    
        """Terminate the application.

        Performs these shutdown operations in order:
        1. Closes the RS232 connection to the Newport stage
        2. Releases any system resources
        3. Closes the main application window

        Safety Features:
        - Ensures proper hardware disconnection
        - Prevents resource leaks
        - Follows Qt's window closing protocol

        Note:
        - Always call this instead of directly closing the window
        - Pending measurements are aborted during shutdown
        - Unsaved data will be lost
        """
        try:
            self.thread.smc.rs232_close()   
        finally:
            self.close()

if __name__ == '__main__':
    app = qtw.QApplication([])
    tela = GeneralFemto()
    tela.show()
    app.exec_()