# -*- coding: utf-8 -*-
"""
Created on Wed May 30 19:48:04 2018

@author: JohannesMHeinrich

-------------------------------------------------------------------------------
This is a collection of functions which are handy to analyse the monitoring
.txt-files of the experiment at the Laboratoire Kastler Brossel in Paris.
-------------------------------------------------------------------------------
  
- import_txt_file:
  import txt file with monitoring of parameters
  
- prepare_monitoring_data:
  prepares the monitoring data for plotting, especially the time
  
- transform_hh_mm_ss_to_ss:
  transform hhmmss to seconds
  
- get_columns:
  extract the columns to plot
  
- get_Uendc_and_U0:
  get Uendc and U0
  
- nu_626_to_detuning_313:
  transform the data from the wavemeter to the detuning of the 313 beam
  
-------------------------------------------------------------------------------
This is a collection of functions to analyse .asc-files containing the data of
Be+ fluorescence images obtained with EMCCD cameras of the experiment at the
Laboratoire Kastler Brossel in Paris.
-------------------------------------------------------------------------------

- import_asc_file:
  import data and format to array of floats
  
- get_projection_along_x:
  get the projection of the fluorescence image along one axis
  
- get_projection_along_y:
  see above
  
- data_rotate:
  rotates the image by +90 degrees
  
- data_filter:
  filters the data with a threshold which is scaled by a factor
  threshold_factor
  
- data_map:
  filters the data with a threshold which is scaled by a factor
  threshold_factor
  
- get_canny_edges:
  determines the edges of an image
  
- get_ellipse:
  fit the edges with an ellipse
  
- parametrize_ellipse:
  prepare the fitted ellipse for plotting
    
- get_volumina_ellipse:
  get the volumina occupied by the Be+ ions as if there are no impurities
  
- ion_density:
  get ion density for trap parameters and mass
  
- fit_projection:
  fit projection of fluorescence and determine missing ion number
  
- get_timestamp_from_name:
  get timestamp of image from name of image
  
  
"""

import csv
import numpy as np
import matplotlib as plt

from skimage.feature import canny
import cv2
from scipy.integrate import simps

### FUNDAMENTAL CONSTANTS #####################################################
el_charge = 1.60217662*10**-19
atomic_mass = 1.6605390*10**-27
epsilon_0 = 8.854187817*10**-12
k_boltzmann = 1.38064852*10**-23
###############################################################################



### import txt file with monitoring of parameters #############################
def import_txt_file(filename):
    
    ### read the file
    with open(filename) as inputfile:
        data_import = list(csv.reader(inputfile))
     
    ### format the data into an array of floats
    data = []
    for i in range(len(data_import)):
        
        line = data_import[i][:-1]
        line_float = []
        
        for j in range(len(line)):
            line_float.append(float(line[j]))
            
        data.append(line_float)
    
    return data
###############################################################################



### prepares the monitoring data for plotting, especially the time ############
def prepare_monitoring_data(data_in):
    
    t_start_seconds = transform_hh_mm_ss_to_ss(data_in[0][0], data_in[0][1], data_in[0][2])    
    t_stop_seconds = transform_hh_mm_ss_to_ss(data_in[-1][0], data_in[-1][1], data_in[-1][2])
    
    ### format the data into an array of floats
    data = []
    for i in range(len(data_in)):
        
        t_s = transform_hh_mm_ss_to_ss(data_in[i][0], data_in[i][1], data_in[i][2])
        line = [t_s - t_start_seconds] + data_in[i][3:]
            
        data.append(line)
    
    return data
###############################################################################
    


### transform hhmmss to seconds ###############################################
def transform_hh_mm_ss_to_ss(hh, mm, ss):
    
    t_s = hh*3600 + mm*60 + ss
    
    return t_s
###############################################################################



### extract the columns to plot ###############################################
def get_columns(data_in, x, y):
    
    data_x = []
    data_y = []
    
    for i in range(len(data_in)):
        data_x.append(data_in[i][x])
        data_y.append(data_in[i][y])
    
    return data_x, data_y
###############################################################################
    


### get Uendc and U0 ##########################################################
def get_Uendc_and_U0(data_in):
    
    data_t = []
    data_Uendc = []
    data_U0 = []
    
    for i in range(len(data_in)):
        
        data_t.append(data_in[i][0])
        
        Ue = np.mean([data_in[i][2],data_in[i][4],data_in[i][5],data_in[i][7]])
        Urf = np.mean([data_in[i][1],data_in[i][8]])
        Ucenter = np.mean([data_in[i][3],data_in[i][6]])
        
        data_Uendc.append(np.abs(Ue-Ucenter))
        data_U0.append(np.abs(Urf-Ucenter))
    
    return data_t, data_Uendc, data_U0
###############################################################################



### transform the data from the wavemeter to the detuning of the 313 beam #####
def nu_626_to_detuning_313(data_in):
    
    data_t = []
    nu_detuning = []
    
    for i in range(len(data_in)):
        
        data_t.append(data_in[i][0])
        
        nu = (2 * data_in[i][15] * 1000000 - 957397084.8 - 3.0/8.0*1250)
        nu_detuning.append(nu)

    return data_t, nu_detuning
###############################################################################
    


###############################################################################
###############################################################################
###############################################################################
    


### import data and format to array of floats #################################
def import_asc_file(filename):
    
    ### read the file
    with open(filename) as inputfile:
        data_import = list(csv.reader(inputfile))
        
    ### format the data into an array of floats
    data = []
    for i in range(len(data_import)):
        
        line = data_import[i][1:-1]
        line_float = []
        
        for j in range(len(line)):
            line_float.append(float(line[j]))
            
        data.append(line_float)
    
    return data
###############################################################################
    


### get the projection of the fluorescence image along one axis ###############
def get_projection_along_x(data_in):
    
    data_out = []

    for i in range(len(data_in)):
        data_out.append(sum(data_in[i]))
           
    return data_out
###############################################################################



### get the projection of the fluorescence image along one axis ###############
def get_projection_along_y(data_in):
    
    data = data_rotate(data_in)
    data_out = []

    for i in range(len(data)):
        data_out.append(sum(data[i]))
           
    return data_out
###############################################################################
    


### rotates the image by +90 degrees ##########################################
def data_rotate(data_in):
    
    ### swap axes
    data = np.swapaxes(data_in,0,1)
    
    return data
###############################################################################
    


### filters the data with a threshold which is scaled by a factor #############
### threshold_factor ##########################################################
def data_filter(data_in, threshold_factor):
    
    ### determine the threshold. to do so, take an area in the corner which
    ### SHOULD be dark, and get the average in this area. the average is then
    ### scaled with the threshold_factor
    dark_area = []
    for i in range(128):
        for j in range(128):
            dark_area.append(data_in[i][j])
    fluo_threshold = threshold_factor * (sum(dark_area)/len(dark_area))
    
    ### filter the data with the threshold
    data = []
    for i in range(len(data_in)):
        vec = []
        for j in range(len(data_in[i])):
            if data_in[i][j] < fluo_threshold:
                vec.append(0.0)
            else:
                vec.append(data_in[i][j])
        data.append(vec)
    
    return data
###############################################################################
    


### filters the data with a threshold which is scaled by a factor #############
### threshold_factor ##########################################################
def data_map(data_in, threshold_factor):
    
    ### determine the threshold. to do so, take an area in the corner which
    ### SHOULD be dark, and get the average in this area. the average is then
    ### scaled with the threshold_factor
    dark_area = []
    for i in range(128):
        for j in range(128):
            dark_area.append(data_in[i][j])
    fluo_threshold = threshold_factor * (sum(dark_area)/len(dark_area))
    
    ### filter the data with the threshold
    data = []
    for i in range(len(data_in)):
        vec = []
        for j in range(len(data_in[i])):
            if data_in[i][j] < fluo_threshold:
                vec.append(0.0)
            else:
                vec.append(1.0)
        data.append(vec)
    
    return data
###############################################################################



### determines the edges of an image ##########################################
def get_canny_edges(data_in, sigma, low_threshold, high_threshold):
    edges = canny(np.array(data_in), sigma, low_threshold, high_threshold)

    return edges
###############################################################################



### fit the edges with an ellipse #############################################
def get_ellipse(data_in):
    points = []
    for i in range(len(data_in)):
        for j in range(len(data_in[i])):
            if data_in[i][j] == True:
                points.append([i,j])
    
    fit_ellipse = cv2.fitEllipse(np.array(points))
    
    fit_ellipse_sorted = [fit_ellipse[0][0], fit_ellipse[0][1], fit_ellipse[1][0]/2.0, fit_ellipse[1][1]/2.0, fit_ellipse[2]]
    
    return fit_ellipse_sorted
###############################################################################



### prepare the fitted ellipse for plotting ###################################
def parametrize_ellipse(data_in):
    ellipse_x = []
    ellipse_y = []
    
    alpha = np.arange(0, 2*np.pi, 0.01)
    
    center_x = data_in[0]
    center_y = data_in[1]

    ell_semi_major_axis = data_in[2]
    ell_semi_minor_axis = data_in[3]
    
    theta = 2*np.pi*data_in[4]/360.0
    
    for i in range(len(alpha)):
        ellipse_x.append(ell_semi_major_axis * np.cos(alpha[i]) * np.cos(theta) - ell_semi_minor_axis * np.sin(alpha[i]) * np.sin(theta) + center_x)
        ellipse_y.append(ell_semi_major_axis * np.cos(alpha[i]) * np.sin(theta) + ell_semi_minor_axis * np.sin(alpha[i]) * np.cos(theta) + center_y)

    return ellipse_x, ellipse_y
###############################################################################



### get the volumina occupied by the Be+ ions as if there are no impurities ####
def get_volumina_ellipse(ellipse, cam_m_per_pixel):
    ell_semi_minor_axis = ellipse[2] * cam_m_per_pixel
    ell_semi_major_axis = ellipse[3] * cam_m_per_pixel
    
    if ell_semi_minor_axis < ell_semi_major_axis:
        ell_volume = 4.0/3.0 * np.pi * ell_semi_minor_axis**2 * ell_semi_major_axis
    else:
        ell_volume = 4.0/3.0 * np.pi * ell_semi_minor_axis * ell_semi_major_axis**2
        
    return ell_volume
###############################################################################  
    


### get ion density for trap parameters and mass ##############################
def ion_density(U_rf_in, m_in, r_0_in, Omega_in):    
    n = (epsilon_0 * U_rf_in**2)/(m_in * r_0_in**4 * Omega_in**2)
    
    return n
###############################################################################



### fit projection of fluorescence and determine missing ion number ###########
def fit_projection(data_in_x, data_in_y, minor, y_center):

    # start and stop values of the fluorescence projection
    x_start = int(y_center - minor)
    x_stop = int(y_center + minor)
    x_center = int(y_center)
    
    # divide the data into two lists to find the maxima in both
    mask_for_a, mask_for_b = [], []
    for i in range(len(data_in_x)):
        if i <= x_center:
            mask_for_a.append(0)
            mask_for_b.append(1)
        elif i > x_center:
            mask_for_a.append(1)
            mask_for_b.append(0)
    
    # create the masked lists to find the maxima
    data_in_y_masked_a = np.ma.masked_array(data_in_y, mask=mask_for_a)
    data_in_y_masked_b = np.ma.masked_array(data_in_y, mask=mask_for_b)
    
    # the indices of the two maxima in the divided lists
    index_max_a = np.ma.argmax(data_in_y_masked_a)
    index_max_b = np.ma.argmax(data_in_y_masked_b)
    
    # the big mask for the fit
    the_mask = []
    for i in range(len(data_in_x)):
        if i >= 0 and i < x_start:
            the_mask.append(1)
        elif i >= x_start and i < index_max_a:
            the_mask.append(0)
        elif i >= index_max_a and i < index_max_b:
            the_mask.append(1)
        elif i >= index_max_b and i < x_stop:
            the_mask.append(0)
        elif i >= x_stop and i <= len(data_in_x):
            the_mask.append(1)
        else:
            print('problem')
    
    # mask the arrays        
    data_in_x_masked = np.ma.masked_array(data_in_x, mask=the_mask)
    data_in_y_masked = np.ma.masked_array(data_in_y, mask=the_mask)
    
    # fit the arrays
    the_fit = np.ma.polyfit(data_in_x_masked, data_in_y_masked, 2)
    
    p = np.poly1d(the_fit)
    
    # create the data to be plotted
    fit_x, fit_y = [], []
    for i in range(len(data_in_x)):
        fit_x.append(data_in_x[i])
        fit_y.append(p(data_in_x[i]))
    
    # cut the values if the fit is smaller than zero
    fit_x_positive, fit_y_positive = [], []
    for i in range(len(fit_x)):
        if fit_y[i] > 0:  
            fit_x_positive.append(fit_x[i])
            fit_y_positive.append(fit_y[i])
            
    integral_fit = simps(fit_y_positive, fit_x_positive)
    integral_data = simps(data_in_y[x_start:x_stop], data_in_x[x_start:x_stop])
    
    fraction = (integral_fit-integral_data)/integral_fit
        
    return fit_x_positive, fit_y_positive, fraction, index_max_a, index_max_b
###############################################################################



### et timestamp of image from name of image ##################################
def get_timestamp_from_name(name):
    
    in_sep = max(loc for loc, val in enumerate(name) if val == '/')
    
    str_time = name[in_sep+1:in_sep+18]
    
    yyyy = str_time[0:4]
    mm = str_time[5:7]
    dd = str_time[8:10]
    
    hh = str_time[11:13]
    MM = str_time[13:15]
    ss = str_time[15:17]
    
    timestamp = str(dd) + '/' + str(mm) + '/' + str(yyyy) + ' ' + str(hh) + ':' + str(MM) + ':' + str(ss)

    return timestamp
###############################################################################






###############################################################################
def save_cloud_fig(data_in, x1, x2, y1, y2, font_size_label, name):
    
    
    in_sep = max(loc for loc, val in enumerate(name) if val == '/')
    
    str_time = name[in_sep+1:in_sep+18]
    
    yyyy = str_time[0:4]
    mm = str_time[5:7]
    dd = str_time[8:10]
    
    hh = str_time[11:13]
    MM = str_time[13:15]
    ss = str_time[15:17]
    
    timestamp = str(dd) + '/' + str(mm) + '/' + str(yyyy) + ' ' + str(hh) + ':' + str(MM) + ':' + str(ss)
    #-----------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------#
    fig = plt.figure(1)
    #-----------------------------------------------------------------------------#
    
    fig_cloud = plt.subplot2grid((6,2), (2,1), rowspan = 4, colspan=1)
    #-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -#
    plt.imshow(data_in, aspect = 1)
    
    plt.title(timestamp)
    #-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -#
    plt.axis([x1, x2, y1, y2])
    plt.xlabel(r'$pixel$',fontsize = font_size_label)
    fig_cloud.xaxis.set_label_position("bottom")
    #plt.xticks([0,512,1024], fontsize = font_size_ticks)
    fig_cloud.xaxis.tick_bottom()
    
    plt.ylabel(r'$pixel$',fontsize = font_size_label)
    fig_cloud.yaxis.set_label_position("right")
    #plt.yticks([0,512,1024], fontsize = font_size_ticks)
    fig_cloud.yaxis.tick_right()
    #-----------------------------------------------------------------------------#
    
    #-----------------------------------------------------------------------------#
    fig.savefig(str(name) + '.png', bbox_inches='tight',dpi=300)
    #-----------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------#
###############################################################################