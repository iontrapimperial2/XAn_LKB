# -*- coding: utf-8 -*-
"""
Created on Sun Jun 04 12:13:33 2017

@author: JohannesMHeinrich
"""



import numpy as np

from apscheduler.schedulers.qt import QtScheduler # --------------------------- to use the scheduler for the execution of jobs
from time import localtime, strftime # ---------------------------------------- for the right format of time values
import datetime # ------------------------------------------------------------- for the monitoring
import statistics

from crystal_analysis_functions_v6 import * # --------------------------------- collection of analysis functions



### FUNDAMENTAL CONSTANTS #####################################################
epsilon_0 = 8.854187817*10**-12
k_boltzmann = 1.38064852*10**-23
###############################################################################



### FUNDAMENTAL PARAMETERS ####################################################

Omega = 2*np.pi * 13.335*10**6
R = 0.0035
kappa = 0.9945
r_0 = kappa * R
###############################################################################





###############################################################################
###############################################################################
###############################################################################
###########                                                            ########
###########               THE MAIN PROGRAMM                            ########
###########                                                            ########
###############################################################################
###############################################################################
###############################################################################

# starts the scheduler for the program ----------------------------------------
program_scheduler = QtScheduler()
program_scheduler.start()
# -----------------------------------------------------------------------------

class c_program:
    def __init__(self):
        
        # global parameters --------------------- #
        self.el_charge = 1.60217662*10**-19
        self.atomic_mass = 1.6605390*10**-27
        self.m_H2 = 2 * self.atomic_mass
        self.m_H3 = 3 * self.atomic_mass
        self.m_Be = 9 * self.atomic_mass
        self.magnification = 0.000002


        # for the monitoring tab ---------------- #
        self.filename_monitoring = '1'
        self.data_monitoring_raw = []
        self.data_monitoring_changed_timescale = []     
        self.data_monitoring_all = []
        
        
        
        # for the image tab --------------------- #
        self.filename_image = '1'
        self.timestamp = str('01/01/1900 00:00:00')
        
        self.data_image_raw = []    
        self.data_projection_top = []
        self.data_projection_right = []
        
        self.filtering_threshold_factor = 0.0
        self.data_image_filtered = []
        
        self.cutoff_factor = 1.0
        self.sigma = 5.0
        self.low_threshold = 0.5
        self.high_threshold = 0.8
        self.data_image_edges = []
        
        self.ellipse = []
        self.ellipse_x, self.ellipse_y = [], []
        self.ellipse_volume = 0.0
        
        self.Be_density = 0.0
        self.Be_number = 0
        
        self.image_mass = 0
        self.image_r_0 = 0
        self.image_frequency = 0
        
        self.projection_fit_x, self.projection_fit_y = [], []
        self.fraction = 0.0
        self.index_max_a, self.index_max_b = 0, 0
        
        self.Be_number_corrected = 0
        self.dark_ions_number = 0
        
        
        
        # for multiple images
        self.filenames_multiple_images = []
        
        self.filenames_selected_images = []
        
            
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#        
    #~~ FUNCTIONS OF THE MAIN PROGRAM ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# 

    #~~ import the data - see crystal_analysis_functions_v5 for more ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#      
    def XAn_import_monitoring_file(self, filename):    
        self.data_monitoring_raw = import_txt_file(filename)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
    #~~ prepare the data - see crystal_analysis_functions_v5 for more ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#      
    def XAn_prepare_monitoring_data(self, filename):    
        self.data_monitoring_changed_timescale = prepare_monitoring_data(filename)
        
        t, dc_el_1 = get_columns(self.data_monitoring_changed_timescale, 0, 1)
        t, dc_el_2 = get_columns(self.data_monitoring_changed_timescale, 0, 2)
        t, dc_el_3 = get_columns(self.data_monitoring_changed_timescale, 0, 3)
        t, dc_el_4 = get_columns(self.data_monitoring_changed_timescale, 0, 4)
        t, dc_el_5 = get_columns(self.data_monitoring_changed_timescale, 0, 5)
        t, dc_el_6 = get_columns(self.data_monitoring_changed_timescale, 0, 6)
        t, dc_el_7 = get_columns(self.data_monitoring_changed_timescale, 0, 7)
        t, dc_el_8 = get_columns(self.data_monitoring_changed_timescale, 0, 8)
        t, rf_ampl = get_columns(self.data_monitoring_changed_timescale, 0, 9)
        t, rf_freq = get_columns(self.data_monitoring_changed_timescale, 0, 10)
        t, i_oven = get_columns(self.data_monitoring_changed_timescale, 0, 11)     
        t, i_egun = get_columns(self.data_monitoring_changed_timescale, 0, 12)
        t, u_egun_filament = get_columns(self.data_monitoring_changed_timescale, 0, 13)
        t, u_egun_wehnelt = get_columns(self.data_monitoring_changed_timescale, 0, 14)    
        t, freq_313 = get_columns(self.data_monitoring_changed_timescale, 0, 15)
        t, pressure = get_columns(self.data_monitoring_changed_timescale, 0, 16)
        t, cam_temp = get_columns(self.data_monitoring_changed_timescale, 0, 17)
        t, cam_exp = get_columns(self.data_monitoring_changed_timescale, 0, 18)
        t, cam_gain = get_columns(self.data_monitoring_changed_timescale, 0, 19)
        
        # operations on that
        t, U_endc, U_0 = get_Uendc_and_U0(self.data_monitoring_changed_timescale)
        t, freq_313_relative = nu_626_to_detuning_313(self.data_monitoring_changed_timescale)
        
        self.data_monitoring_all = [t, dc_el_1, dc_el_2, dc_el_3, dc_el_4, dc_el_5, dc_el_6, dc_el_7, dc_el_8, rf_ampl, rf_freq, i_oven, i_egun, u_egun_filament, u_egun_wehnelt, freq_313, pressure, cam_temp, cam_exp, cam_gain, U_endc, U_0, freq_313_relative]
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
    
    
    
    
    #~~ import the data - see crystal_analysis_functions_v5 for more ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#      
    def XAn_import_image_file(self, filename):    
        self.data_image_raw = import_asc_file(filename)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    #~~ import the data - see crystal_analysis_functions_v5 for more ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#      
    def XAn_get_timestamp_from_name(self, filename):    
        self.timestamp = get_timestamp_from_name(filename)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#    
    
    #~~ get the projections - see crystal_analysis_functions_v5 for more ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#      
    def XAn_get_projections(self, data_in):    
        self.data_projection_top = get_projection_along_x(data_in)
        self.data_projection_right = get_projection_along_y(data_in)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#    
    
    #~~ rotate the data and redo the projections - see crystal_analysis_functions_v5 for more ~~~~~~~~~#      
    def XAn_rotate_image_file(self):    
        self.data_image_raw = data_rotate(self.data_image_raw)
        self.XAn_get_projections(self.data_image_raw)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#    
    
    #~~ filter the data and redo the projections - see crystal_analysis_functions_v5 for more ~~~~~~~~~#      
    def XAn_filter_image_file(self, threshold_factor):    
        self.data_image_filtered = data_map(self.data_image_raw, threshold_factor)
        self.XAn_get_projections(self.data_image_filtered)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#     

    #~~ get the edges of the ellipse - see crystal_analysis_functions_v5 for more ~~~~~~~~~~~~~~~~~~~~~#      
    def XAn_edges_image_file(self, cutoff_factor, sigma, low_threshold, high_threshold):        
        self.data_image_edges = get_canny_edges(self.data_image_filtered, sigma, low_threshold, high_threshold)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# 
    
    #~~ get the ellipse - see crystal_analysis_functions_v5 for more ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#      
    def XAn_ellipse_image_file(self, threshold, accuracy, min_size, max_size):
        self.ellipse = get_ellipse(self.data_image_edges)
        self.ellipse_x, self.ellipse_y = parametrize_ellipse(self.ellipse)
        self.ellipse_volume = get_volumina_ellipse(self.ellipse, self.magnification)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#     

    #~~ get the number of Be+ - see crystal_analysis_functions_v5 for more ~~~~~~~~~~~~~~~~~~~~~~~~~~~~#      
    def XAn_Be_number_image_file(self, U_rf_in, m_in, r_0_in, Omega_in):
        self.Be_density = ion_density(U_rf_in, m_in, r_0_in, Omega_in)    
        self.Be_number = self.Be_density * self.ellipse_volume
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#          
    
    #~~ fit the projections - see crystal_analysis_functions_v5 for more ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#      
    def XAn_fit_projection(self, data_in_x, data_in_y, minor, y_center):
        temp = data_filter(self.data_image_raw, 1.5)
        self.XAn_get_projections(temp)
        self.projection_fit_x, self.projection_fit_y, self.fraction, self.index_max_a, self.index_max_b = fit_projection(np.arange(0,len(self.data_projection_right)), self.data_projection_right, minor, y_center)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#     
  
    #~~ correct the ion number and get dark ions - see crystal_analysis_functions_v5 for more ~~~~~~~~~#      
    def XAn_correct_ion_numbers(self):
        missing_ion_number = self.Be_number * self.fraction
        self.dark_ions_number = int(missing_ion_number)
        self.Be_number_corrected = int(self.Be_number - missing_ion_number)
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#    
    
    






    def XAn_multiple(self): 

        number_dark_ions = []
        
        for i in range(len(self.filenames_multiple_images)):
            ### load data
            try:
                self.XAn_import_image_file(self.filenames_multiple_images[i])
            except FileNotFoundError:
                print('nothing found to that name')
            
            
            
            self.XAn_filter_image_file(self.filtering_threshold_factor)            
            
            self.XAn_edges_image_file(self.cutoff_factor, self.sigma, self.low_threshold, self.high_threshold)
 
            self.XAn_ellipse_image_file(threshold=100, accuracy=20, min_size=50, max_size=600)
            
            self.XAn_Be_number_image_file(self.image_ampl, self.image_mass, self.image_r_0, self.image_frequency)

            self.XAn_fit_projection(np.arange(0,len(self.data_projection_right)), self.data_projection_right, self.ellipse[2], self.ellipse[1])
            
            self.XAn_correct_ion_numbers()
            
            
            number_dark_ions.append(self.dark_ions_number)
            
            print(str(i) + ' of ' + str(len(self.filenames_multiple_images)) + ' done: ' + str(self.dark_ions_number))
        
        num_dark_ions_splitted = [number_dark_ions[x:x+10] for x in range(0, len(number_dark_ions), 10)]
        
        num_with_uncertainties = []
        for i in range(len(num_dark_ions_splitted)):
            m = statistics.mean(num_dark_ions_splitted[i])
            dev = statistics.stdev(num_dark_ions_splitted[i])
            num_with_uncertainties.append([m, dev])
        
        print(num_with_uncertainties)
        
        with open('results_images.txt', "a") as myfile:
            for i in range(len(num_with_uncertainties)):
                myfile.write(str(num_with_uncertainties[i]) + ',')
                
        with open('results_images_individual.txt', "a") as myfile:
            for i in range(len(number_dark_ions)):
                myfile.write(str(number_dark_ions[i]) + ',')
    
    
#    #~~ import the data - see crystal_analysis_functions_v5 for more ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#    def XAn_save_cloud_image(self, data_in, x1, x2, y1, y2, font_size_label, name):
#        save_cloud_fig(data_in, x1, x2, y1, y2, font_size_label, name)
#    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#