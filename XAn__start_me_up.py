# -*- coding: utf-8 -*-
"""
Created on Sun Jun 04 12:14:27 2017

@author: JohannesMHeinrich
"""

import sys # ------------------------------------------------------------------ import for stuff i guess? i don't really know... 
from PyQt5 import QtCore, QtGui, QtWidgets # ---------------------------------- imports for the GUI
from PyQt5.QtWidgets import QFileDialog
 
import time # ----------------------------------------------------------------- time
from apscheduler.schedulers.qt import QtScheduler # --------------------------- similar to above
import pyqtgraph as pg # ------------------------------------------------------ for the plots
import numpy as np

from XAn_gui import Ui_XAn # -------------------------------------------------- import the layout generated with QtDesigner
from XAn_main_program import c_program # -------------------------------------- the program which collects the controll over all the devices

import threading

## global style options for the plots -----------------------------------------
brush_background = (255,255,255,255) #----------------------------------------- background

brush_red = (255,0,0,255) #---------------------------------------------------- red for measured values
brush_blue = (0,0,255,255)
brush_green = (0,255,0,255)

redPen = pg.mkPen(color=brush_red, width=1) #-------------------------------- same like brush_red
bluePen = pg.mkPen(color=brush_blue, width=1)
greenPen = pg.mkPen(color=brush_green, width=1)
pens = [redPen, bluePen, greenPen]

labelStyle_l = {'color': '#000', 'font-size': '12pt'} #------------------------ big label

                



###############################################################################
###############################################################################
###############################################################################
###########                                                            ########
###########               THE WINDOW CLASS                             ########
###########                                                            ########
###############################################################################
###############################################################################
###############################################################################


# starts the scheduler for the program ----------------------------------------
starttime=time.time()
scheduler = QtScheduler()
scheduler.start()
# -----------------------------------------------------------------------------

class window(Ui_XAn):
    def __init__(self, dialog_A, the_program):
        Ui_XAn.__init__(self)
        self.setupUi(dialog_A)
        
###############################################################################
###############################################################################
###############################################################################
###### the first part of the class sets up the layout of the program.   #######
###### the PLOTS are placed and the PUSH BUTTONS are connected with the #######
###### functions which are defined further below in the class           #######
###############################################################################
###############################################################################
###############################################################################
               
   
     
###############################################################################
####### PLOTS monitoring tab ##################################################
###############################################################################
        
        #---------------- PLOT for monitoring 1 ------------------------------#
        self.plot_mon_01 = pg.PlotWidget(name='Plot_mon_01')
        self.plot_mon_01.setBackground(background=brush_background)
        self.plot_mon_01.showGrid(x=True,y=True)
        self.verticalLayout_mon_01.addWidget(self.plot_mon_01)       
        #---------------------------------------------------------------------#
        
        #---------------- PLOT for monitoring 2 ------------------------------#
        self.plot_mon_02 = pg.PlotWidget(name='Plot_mon_02')
        self.plot_mon_02.setBackground(background=brush_background)
        self.plot_mon_02.showGrid(x=True,y=True)
        self.verticalLayout_mon_02.addWidget(self.plot_mon_02)       
        #---------------------------------------------------------------------#

        #---------------- PLOT for monitoring 3 ------------------------------#
        self.plot_mon_03 = pg.PlotWidget(name='Plot_mon_03')
        self.plot_mon_03.setBackground(background=brush_background)
        self.plot_mon_03.showGrid(x=True,y=True)
        self.verticalLayout_mon_03.addWidget(self.plot_mon_03)       
        #---------------------------------------------------------------------#

        #---------------- PLOT for monitoring 4 ------------------------------#
        self.plot_mon_04 = pg.PlotWidget(name='Plot_mon_04')
        self.plot_mon_04.setBackground(background=brush_background)
        self.plot_mon_04.showGrid(x=True,y=True)
        self.verticalLayout_mon_04.addWidget(self.plot_mon_04)       
        #---------------------------------------------------------------------#

        #---------------- PLOT for monitoring 5 ------------------------------#
        self.plot_mon_05 = pg.PlotWidget(name='Plot_mon_05')
        self.plot_mon_05.setBackground(background=brush_background)
        self.plot_mon_05.showGrid(x=True,y=True)
        self.verticalLayout_mon_05.addWidget(self.plot_mon_05)       
        #---------------------------------------------------------------------#

        #---------------- PLOT for monitoring 6 ------------------------------#
        self.plot_mon_06 = pg.PlotWidget(name='Plot_mon_06')
        self.plot_mon_06.setBackground(background=brush_background)
        self.plot_mon_06.showGrid(x=True,y=True)
        self.verticalLayout_mon_06.addWidget(self.plot_mon_06)       
        #---------------------------------------------------------------------#        

             
        
        #================ PUSH BUTTONS for PLOTS monitoring tab ==============#          
        self.pushButton_monitoring_browse_data.clicked.connect(self.browse_data)
        self.pushButton_monitoring_load_data.clicked.connect(self.import_monitoring_file)
        
        self.pushButton_plot_mon_01.clicked.connect(self.f_plot_mon_01)
        self.pushButton_plot_mon_02.clicked.connect(self.f_plot_mon_02)
        self.pushButton_plot_mon_03.clicked.connect(self.f_plot_mon_03)
        self.pushButton_plot_mon_04.clicked.connect(self.f_plot_mon_04)
        self.pushButton_plot_mon_05.clicked.connect(self.f_plot_mon_05)
        self.pushButton_plot_mon_06.clicked.connect(self.f_plot_mon_06)
        self.pushButton_plot_mon_all.clicked.connect(self.f_plot_mon_all)
        
        self.pushButton_plot_mon_01_clear.clicked.connect(self.f_plot_mon_clear_01)
        self.pushButton_plot_mon_02_clear.clicked.connect(self.f_plot_mon_clear_02)
        self.pushButton_plot_mon_03_clear.clicked.connect(self.f_plot_mon_clear_03)
        self.pushButton_plot_mon_04_clear.clicked.connect(self.f_plot_mon_clear_04)
        self.pushButton_plot_mon_05_clear.clicked.connect(self.f_plot_mon_clear_05)
        self.pushButton_plot_mon_06_clear.clicked.connect(self.f_plot_mon_clear_06)
        self.pushButton_plot_mon_clear_all.clicked.connect(self.f_plot_mon_clear_all)
        #=====================================================================#



###############################################################################
####### CAMERA image tab ######################################################
###############################################################################

        #---------------- PLOT for CC projection #----------------------------#GraphicsWindow
        self.image_CC = pg.GraphicsLayoutWidget()
        self.image_CC.ci.layout.setColumnStretchFactor(0, 2)
        self.image_CC.ci.layout.setColumnStretchFactor(1, 1)
        self.image_CC.ci.layout.setRowStretchFactor(0, 1)
        self.image_CC.ci.layout.setRowStretchFactor(1, 2)
        self.verticalLayout_image.addWidget(self.image_CC)
        
        self.plot_image_CC = self.image_CC.addPlot(1, 0, rowspan=1, colspan=1)
        self.plot_image_CC.setAspectLocked()

        self.projection_top = self.image_CC.addPlot(0, 0, rowspan=1, colspan=1)
        self.projection_top.showGrid(x = True, y = True, alpha = 0.75) 
        self.projection_top.setXLink(self.plot_image_CC)
        
        self.projection_side = self.image_CC.addPlot(1, 1, rowspan=1, colspan=1)
        self.projection_side.showGrid(x = True, y = True, alpha = 0.75)
        self.projection_side.setYLink(self.plot_image_CC)
        
        self.plot_timestamp = self.image_CC.addPlot(0, 1, rowspan=1, colspan=1)
        self.plot_timestamp.hideAxis('bottom')
        self.plot_timestamp.hideAxis('left')
        #---------------------------------------------------------------------# 



        #================ PUSH BUTTONS for CAMERA image tab ==================#          
        self.pushButton_image_browse_data.clicked.connect(self.browse_image)
        self.pushButton_image_load_data.clicked.connect(self.import_image_file)
        
        self.pushButton_image_rotate.clicked.connect(self.rotate_image_file)
        self.pushButton_image_filter.clicked.connect(self.filter_image_file)
        self.pushButton_image_edges.clicked.connect(self.edges_image_file)
        
        self.pushButton_image_ellipse.clicked.connect(self.ellipse_image_file)
        
        self.pushButton_image_get_ion_number.clicked.connect(self.get_ion_number)
        
        self.pushButton_image_inner_structure.clicked.connect(self.get_inner_structure)
        #=====================================================================#



###############################################################################
####### image series tab ######################################################
###############################################################################
            
        #---------------- PLOT -----------------------------------------------#
        self.plot_results = pg.PlotWidget(name='Plot_res')
        self.plot_results.setBackground(background=brush_background)
        self.plot_results.showGrid(x=True,y=True)
        self.verticalLayout_series_results.addWidget(self.plot_results)       
        #---------------------------------------------------------------------#


        #================ PUSH BUTTONS for image series tab ==================#
        self.pushButton_image_browse_multiple_data.clicked.connect(self.browse_multiple_images)
        self.pushButton_image_save_series.clicked.connect(self.select_images)
        #=====================================================================#

        



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~ the second part of the class contains all the FUNCTIONS which are  ~~~~#
#~~~~~ triggerered when the different push buttons are pressed. there are ~~~~#
#~~~~~ more functions dedicated to permanet monitoring and backgroundjobs ~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# 
    
###############################################################################
####### monitoring tab ########################################################
###############################################################################
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def browse_data(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog    
        the_program.filename_monitoring, _ = QFileDialog.getOpenFileName(None,"import data", "","all files (*);; asc files (*.asc);; txt files (*.txt)", options=options)
        
        if the_program.filename_monitoring:
            self.lineEdit_monitoring_load_data.setText(the_program.filename_monitoring)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def import_monitoring_file(self):
        
        ### read filename
        the_program.filename_monitoring = str(self.lineEdit_monitoring_load_data.text())
        
        ### load and prepare data
        try:
            the_program.XAn_import_monitoring_file(the_program.filename_monitoring)
            the_program.XAn_prepare_monitoring_data(the_program.data_monitoring_raw)
        except FileNotFoundError:
            print('nothing found to that name')
        except UnicodeDecodeError:
            print('not a suitable file format selected')
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def f_plot_mon_01(self):
        x = self.comboBox_plot_1_x.currentIndex()
        y = self.comboBox_plot_1_y.currentIndex()
        pen_color = (len(self.plot_mon_01.listDataItems()) + 3) % 3
        self.plotted_mon_01 = self.plot_mon_01.plot(the_program.data_monitoring_all[x],the_program.data_monitoring_all[y], pen = pens[pen_color], name = 'plot_01')

    def f_plot_mon_02(self):
        x = self.comboBox_plot_2_x.currentIndex()
        y = self.comboBox_plot_2_y.currentIndex()
        pen_color = (len(self.plot_mon_02.listDataItems()) + 3) % 3
        self.plotted_mon_02 = self.plot_mon_02.plot(the_program.data_monitoring_all[x],the_program.data_monitoring_all[y], pen = pens[pen_color], name = 'plot_02')

    def f_plot_mon_03(self):
        x = self.comboBox_plot_3_x.currentIndex()
        y = self.comboBox_plot_3_y.currentIndex()
        pen_color = (len(self.plot_mon_03.listDataItems()) + 3) % 3
        self.plotted_mon_03 = self.plot_mon_03.plot(the_program.data_monitoring_all[x],the_program.data_monitoring_all[y], pen = pens[pen_color], name = 'plot_02')
 
    def f_plot_mon_04(self):
        x = self.comboBox_plot_4_x.currentIndex()
        y = self.comboBox_plot_4_y.currentIndex()
        pen_color = (len(self.plot_mon_04.listDataItems()) + 3) % 3
        self.plotted_mon_04 = self.plot_mon_04.plot(the_program.data_monitoring_all[x],the_program.data_monitoring_all[y], pen = pens[pen_color], name = 'plot_02')
 
    def f_plot_mon_05(self):
        x = self.comboBox_plot_5_x.currentIndex()
        y = self.comboBox_plot_5_y.currentIndex()
        pen_color = (len(self.plot_mon_05.listDataItems()) + 3) % 3
        self.plotted_mon_05 = self.plot_mon_05.plot(the_program.data_monitoring_all[x],the_program.data_monitoring_all[y], pen = pens[pen_color], name = 'plot_02')
 
    def f_plot_mon_06(self):
        x = self.comboBox_plot_6_x.currentIndex()
        y = self.comboBox_plot_6_y.currentIndex()
        pen_color = (len(self.plot_mon_06.listDataItems()) + 3) % 3
        self.plotted_mon_06 = self.plot_mon_06.plot(the_program.data_monitoring_all[x],the_program.data_monitoring_all[y], pen = pens[pen_color], name = 'plot_02')
        
    def f_plot_mon_all(self):
        self.f_plot_mon_01()
        self.f_plot_mon_02()
        self.f_plot_mon_03()
        self.f_plot_mon_04()
        self.f_plot_mon_05()
        self.f_plot_mon_06()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#    
    def f_plot_mon_clear_01(self):
        self.plot_mon_01.clear()
        
    def f_plot_mon_clear_02(self):
        self.plot_mon_02.clear()
        
    def f_plot_mon_clear_03(self):
        self.plot_mon_03.clear()
        
    def f_plot_mon_clear_04(self):
        self.plot_mon_04.clear()
        
    def f_plot_mon_clear_05(self):
        self.plot_mon_05.clear()
        
    def f_plot_mon_clear_06(self):
        self.plot_mon_06.clear()
        
    def f_plot_mon_clear_all(self):
        self.f_plot_mon_clear_01()
        self.f_plot_mon_clear_02()
        self.f_plot_mon_clear_03()
        self.f_plot_mon_clear_04()
        self.f_plot_mon_clear_05()
        self.f_plot_mon_clear_06()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#    
        


###############################################################################
####### CAMERA image tab ######################################################
###############################################################################

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def browse_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog    
        the_program.filename_image, _ = QFileDialog.getOpenFileName(None,"import image", "","all files (*);; asc files (*.asc);; txt files (*.txt)", options=options)
        
        if the_program.filename_image:
            self.lineEdit_image_load_data.setText(the_program.filename_image)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def import_image_file(self):
        
        ### read filename
        the_program.filename_image = str(self.lineEdit_image_load_data.text())
        the_program.XAn_get_timestamp_from_name(the_program.filename_image)
#        self.plot_timestamp.addItem(pg.TextItem(text=str(the_program.timestamp), color=(255, 0, 0), anchor=(0, 0)))
        
        ### load data
        try:
            the_program.XAn_import_image_file(the_program.filename_image)
        except FileNotFoundError:
            print('nothing found to that name')
            
        ### reshape, transform data and plot
        data = pg.ImageItem(np.array(the_program.data_image_raw).reshape(1024,1024))
        self.plot_image_CC.addItem(data, clear = True)
        
        ### get and plot projections
        the_program.XAn_get_projections(the_program.data_image_raw)    
        self.plotted_projection_top = self.projection_top.plot(np.arange(0,len(the_program.data_projection_top)),the_program.data_projection_top, pen = 'b', clear = True)
        self.plotted_projection_side = self.projection_side.plot(the_program.data_projection_right, np.arange(0,len(the_program.data_projection_right)), pen = 'b', clear = True)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def rotate_image_file(self):
        the_program.XAn_rotate_image_file()
        
        ### reshape, transform data and plot
        data = pg.ImageItem(np.array(the_program.data_image_raw).reshape(1024,1024))
        self.plot_image_CC.addItem(data)
        
        ### replot projections  
        self.plotted_projection_top.setData(np.arange(0,len(the_program.data_projection_top)),the_program.data_projection_top)
        self.plotted_projection_side.setData(the_program.data_projection_right, np.arange(0,len(the_program.data_projection_right)))
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def filter_image_file(self):
        the_program.filtering_threshold_factor = float(self.doubleSpinBox_image_filter_threshold.value())
        the_program.XAn_filter_image_file(the_program.filtering_threshold_factor)
        
        ### reshape, transform data and plot
        data = pg.ImageItem(np.array(the_program.data_image_filtered).reshape(1024,1024))
        self.plot_image_CC.addItem(data)
        
        ### get and plot projections
        self.plotted_projection_top.setData(np.arange(0,len(the_program.data_projection_top)),the_program.data_projection_top)
        self.plotted_projection_side.setData(the_program.data_projection_right, np.arange(0,len(the_program.data_projection_right)))
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def edges_image_file(self):  
        the_program.sigma = self.doubleSpinBox_image_edges_sigma.value()
        the_program.low_threshold = self.doubleSpinBox_image_edges_low_threshold.value()
        the_program.high_threshold = self.doubleSpinBox_image_edges_high_threshold.value()
        
        
        the_program.XAn_edges_image_file(the_program.cutoff_factor, the_program.sigma, the_program.low_threshold, the_program.high_threshold)
        
        ### reshape, transform data and plot
        data = pg.ImageItem(np.array(the_program.data_image_edges).reshape(1024,1024))
        self.plot_image_CC.addItem(data)
        
        ### get and plot projections
        self.plotted_projection_top.setData(np.arange(0,len(the_program.data_projection_top)),the_program.data_projection_top)
        self.plotted_projection_side.setData(the_program.data_projection_right, np.arange(0,len(the_program.data_projection_right)))
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def ellipse_image_file(self):
        the_program.magnification = self.doubleSpinBox_image_magnification.value()
        
        data = pg.ImageItem(np.array(the_program.data_image_raw).reshape(1024,1024))        
        self.plot_image_CC.addItem(data, clear = True)
        
        the_program.XAn_ellipse_image_file(threshold=100, accuracy=20, min_size=50, max_size=600)
        self.plot_image_CC.plot(the_program.ellipse_x, the_program.ellipse_y, pen='b')
        
        self.label_image_volume.setText(str(the_program.ellipse_volume))
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def get_ion_number(self):
        the_program.image_mass = self.spinBox_image_ion_mass.value() * the_program.atomic_mass
        the_program.image_r_0 = self.doubleSpinBox_image_r_0.value()
        the_program.image_frequency = 2 * np.pi * self.doubleSpinBox_image_frequency.value() * 10**6
        the_program.image_ampl = self.doubleSpinBox_image_rf_amplitude.value()
        
        the_program.XAn_Be_number_image_file(the_program.image_ampl, the_program.image_mass, the_program.image_r_0, the_program.image_frequency)

        self.label_image_ion_number.setText(str(int(the_program.Be_number)))
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def get_inner_structure(self):
        the_program.XAn_fit_projection(np.arange(0,len(the_program.data_projection_right)), the_program.data_projection_right, the_program.ellipse[2], the_program.ellipse[1])
        self.plotted_projection_side = self.projection_side.plot(the_program.data_projection_right, np.arange(0,len(the_program.data_projection_right)), pen = 'b', clear = True)
        self.projection_side.plot(the_program.projection_fit_y,the_program.projection_fit_x, pen='r')
        self.projection_side.plot([0,1.05*the_program.data_projection_right[the_program.index_max_a]], [the_program.index_max_a,the_program.index_max_a], pen='w')
        self.projection_side.plot([0,1.05*the_program.data_projection_right[the_program.index_max_b]], [the_program.index_max_b,the_program.index_max_b], pen='w')

        the_program.XAn_correct_ion_numbers()
        self.label_image_fraction.setText(str('{:06.4f}'.format(the_program.fraction)))
        self.label_image_ion_number_corrected.setText(str(the_program.Be_number_corrected))
        self.label_image_ion_number_dark.setText(str(the_program.dark_ions_number))
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#        



###############################################################################
####### image series tab ######################################################
###############################################################################

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def browse_multiple_images(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog    
        the_program.filenames_multiple_images, _ = QFileDialog.getOpenFileNames(None,"import image", "","all files (*);; asc files (*.asc);; txt files (*.txt)", options=options)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#    def create_image_series(self):
#        
#        for i in range(len(the_program.filenames_multiple_images)):
#            ### load data
#            try:
#                the_program.XAn_import_image_file(the_program.filenames_multiple_images[i])
#            except FileNotFoundError:
#                print('nothing found to that name')            
#
#            the_program.XAn_save_cloud_image(the_program.data_image_raw, 0, 1024, 0, 1024, 10, the_program.filenames_multiple_images[i])
#    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def loop(self):
        number_dark_ions = []
        
        for i in range(len(the_program.filenames_multiple_images)):
            ### load data
            try:
                the_program.XAn_import_image_file(the_program.filenames_multiple_images[i])
            except FileNotFoundError:
                print('nothing found to that name')
            
            
            self.filter_image_file()
            self.edges_image_file()
            self.ellipse_image_file()
            self.get_ion_number()
            self.get_inner_structure()
            
            
            number_dark_ions.append(the_program.dark_ions_number)
            
            print(str(i) + ' of ' + str(len(the_program.filenames_multiple_images)) + ' done.')
        number_of_images = np.arange(0,len(the_program.filenames_multiple_images))
        
        self.plotted_results = self.plot_results.plot(number_of_images,number_dark_ions, pen='b', symbol='o', name = 'plot_results', clear = True)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#    




    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def select_images(self): 
        
        the_program.XAn_multiple()
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#





#    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#    def select_images(self): 
#        
#        the_program.filenames_multiple_images
#
#        number_dark_ions = []
#        
#        for i in range(len(the_program.filenames_multiple_images)):
#            ### load data
#            try:
#                the_program.XAn_import_image_file(the_program.filenames_multiple_images[i])
#            except FileNotFoundError:
#                print('nothing found to that name')
#            
#            
#            self.filter_image_file()
#            self.edges_image_file()
#            self.ellipse_image_file()
#            self.get_ion_number()
#            self.get_inner_structure()
#            
#            
#            number_dark_ions.append(the_program.dark_ions_number)
#            
#            print(str(i) + ' of ' + str(len(the_program.filenames_multiple_images)) + ' done.')
#            
#        number_of_images = np.arange(0,len(the_program.filenames_multiple_images))
#        
#        num_dark_ions_splitted = [number_dark_ions[x:x+10] for x in range(0, len(number_dark_ions), 10)]
#        
#        num_with_uncertainties = []
#        for i in range(len(num_dark_ions_splitted)):
#            m = statistics.mean(num_dark_ions_splitted[i])
#            dev = statistics.stdev(num_dark_ions_splitted[i])
#            num_with_uncertainties.append([m, dev])
#        
#        print(num_with_uncertainties)
#        
#        with open('results_images.txt', "a") as myfile:
#            for i in range(len(num_with_uncertainties)):
#                myfile.write(str(num_with_uncertainties[i]) + ',')   
#        
#    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#









###############################################################################
###############################################################################
###############################################################################
######                                                                  #######
######                     STARTING THE MAIN LOOP                       #######
######                                                                  #######
###############################################################################
###############################################################################
###############################################################################



if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    
    # create instance of parameters 
    the_program = c_program()
        
    # set up window   
    dialog_sequ = QtWidgets.QMainWindow()
    prog_sequ = window(dialog_sequ,the_program)    
    dialog_sequ.show()

 
    sys.exit(app.exec_())   