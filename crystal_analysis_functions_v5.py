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
  
- normalize:
  normalize the imported data to be in between 0 and 255
  
- get_canny_edges:
  determines the edges of an image
  
- get_contur:
  determines the contur of an image and fits with an ellipse
  
- scan_for_maxima:
    
- get_lin_fit:
    
- get_fit_to_plot
  
- get_ri_Be:
  get indices of the two maxima in the projection
  
- get_ro_H2:
  get the start and end indices of the inner ion shell depending on mass and
  inner radius of the outer shell
  
- get_volumina:
  get the volumina occupied by the Be+ and H2+ ions
  
- ion_density:
  get ion density for trap parameters and mass
  
- get_sec_frequ_from_crystal_shape:
  to cross check - determine the ratio of the secular frequencies from the 
  shape of the ion crystal
  
"""

import csv
import numpy as np
import matplotlib as plt

from skimage.feature import canny
import cv2

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
    


### normalize the imported data to be in between 0 and 255 ####################
def normalize(data_in, cutoff_factor):
    
    ### find the maximum in the data input
    global_max = 0.0
    for i in range(len(data_in)):        
        row_max = max(data_in[i])
        if row_max > global_max:
            global_max = row_max
        else:
            pass

    cutoff = global_max * cutoff_factor
    
    data_out = []
    for i in range(len(data_in)):
        row = []        
        for j in range(len(data_in[i])):
            if data_in[i][j] > cutoff:
                row.append(255)
            else:
                row.append(int(254.0/cutoff * data_in[i][j]))
        data_out.append(row)
        
    return data_out
###############################################################################



#def get_canny_edges_1(data_in, gradient_threshold_min, gradient_threshold_max):
#    
#    data_out = cv2.Canny(np.uint8(data_in), gradient_threshold_min, gradient_threshold_max)
#
#    return data_out   
###############################################################################
def get_canny_edges(data_in, sigma, low_threshold, high_threshold):
    edges = canny(np.array(data_in), sigma, low_threshold, high_threshold)

    return edges
###############################################################################



#def get_ellipse_1(data_in, threshold, accuracy, min_size, max_size):
#    result = hough_ellipse(data_in, threshold, accuracy, min_size, max_size)
#    result.sort(order='accumulator') 
#    best = list(result[-1])
#    
#    return best
#
#def get_ellipse_2(data_in):
#    points_x, points_y = [], []
#    points = []
#    for i in range(len(data_in)):
#        for j in range(len(data_in[i])):
#            if data_in[i][j] == True:
#                points.append([i,j])
#                points_x.append(i)
#                points_y.append(j)
#                
#    ellipse = EllipseModel()
#    ellipse.estimate(np.array(points))
#
#    res = ellipse.params
#
#    return res, points_x, points_y
#
#def get_ellipse_3(data_in):
#    points_x, points_y = [], []
#    X, Y = [],[]
#    points = []
#    for i in range(len(data_in)):
#        for j in range(len(data_in[i])):
#            if data_in[i][j] == True:
#                points.append([i,j])
#                X.append([i])
#                Y.append([j])
#                points_x.append(i)
#                points_y.append(j)
#    
#    X = np.array(X)
#    Y = np.array(Y)
#    
#    # Formulate and solve the least squares problem ||Ax - b ||^2
#    A = np.hstack([X**2, X * Y, Y**2, X, Y])
#    b = np.ones_like(X)
#    x = np.linalg.lstsq(A, b)[0].squeeze()
#
#    ell_a = x[0]
#    ell_b = x[1]
#    ell_c = x[2]
#    ell_d = x[3]
#    ell_e = x[4]
#    
#    x_center = -ell_c/(2.0 * ell_a)
#    y_center = -ell_d/(2.0 * ell_b)
#    
#    print(x_center)
#    print(y_center)
#
#    return x, points_x, points_y
#
#
#
#def get_ellipse_4(data_in):
#    points_x, points_y = [], []
#    X, Y = [],[]
#    points = []
#    for i in range(len(data_in)):
#        for j in range(len(data_in[i])):
#            if data_in[i][j] == True:
#                points.append([i,j])
#                X.append(float(i))
#                Y.append(float(j))
#                points_x.append(i)
#                points_y.append(j)
#    
#    X = np.array(X)
#    Y = np.array(Y)
#    
#    
#    xmean, ymean = X.mean(), Y.mean()
#    X -= xmean
#    Y -= ymean
#    U, S, V = np.linalg.svd(np.stack((X, Y)))
#    
#    N = len(X)
#    tt = np.linspace(0, 2*np.pi, 1000)
#    circle = np.stack((np.cos(tt), np.sin(tt)))    # unit circle
#    transform = np.sqrt(2/N) * U.dot(np.diag(S))   # transformation matrix
#    fit = transform.dot(circle) + np.array([[xmean], [ymean]])
#    
#    fit_ellipse = cv2.fitEllipse(np.array(points))
#
#    return fit_ellipse, fit[0, :], fit[1, :]
###############################################################################
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



###############################################################################
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



### get the volumina occupied by the Be+ and H2+ ions #########################
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



#from skimage.filters import roberts, sobel, scharr, prewitt
#### get ion density for trap parameters and mass ##############################
#def get_edges(data_in):    
#    data_out = prewitt(np.array(data_in))
#    
#    return data_out
################################################################################



from skimage import exposure
### get ion density for trap parameters and mass ##############################
def stretch_contrast(data_in):
    # Contrast stretching
    p2, p98 = np.percentile(np.array(data_in), (2, 98))
    data_out = exposure.rescale_intensity(np.array(data_in), in_range=(p2, p98))
    
    # Equalization
#    data_out = exposure.equalize_hist(np.array(data_in))
    
    # Adaptive Equalization
#    data_out = exposure.equalize_adapthist(np.array(data_in), clip_limit=0.03)
    
    return data_out
###############################################################################



#from scipy import optimize
################################################################################
#def fit_projection(data_in_x, data_in_y, minor, major, y_center):
#    fitfunc = lambda p, x: p[3] * np.pi * (2.0*p[0])/(2.0*p[1]) * (p[1]**2 - (x-p[2])**2)   # Target function
#    errfunc = lambda p, x, y: fitfunc(p, x) - y                                # Distance to the target function
#
#    print(minor)
#    print(major)    
#    
#    x_start = int(y_center - minor)
#    x_stop = int(y_center + minor)
#    
#    print(x_start)
#    print(x_stop)
#    
#    data_in_x_fit = data_in_x[x_start:x_stop]
#    data_in_y_fit = data_in_y[x_start:x_stop]
#    
#    p0 = [major, minor, y_center, 1000]                                              # Initial guess for the parameters
#    p1, success = optimize.leastsq(errfunc, p0[:], args=(data_in_x_fit, data_in_y_fit))
#    
#    fit = []
#    for i in range(len(data_in_x)):
#        fit.append(fitfunc(p1,data_in_x[i]))
#    
#
#    
#    return p1, success, fit
################################################################################
    





from scipy.integrate import simps
def fit_projection_2(data_in_x, data_in_y, minor, y_center):

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











#### determines the contur of an image and fits with an ellipse ################
#def get_contur(data_in):
#    
#    ### determine contur
#    data_out, contours, hierarchy = cv2.findContours(np.uint8(data_in), 1, 2)
#
#    ### concenate the contours
#    cnt_union = contours[0]
#    for i, cnt in enumerate(contours):
#        if i > 0:
#            cnt_union = np.concatenate((cnt_union, cnt), axis=0)
#            
#    ### fit the contur with an ellipse
#    fit_ellipse = cv2.fitEllipse(cnt_union)
#           
#    return data_out, fit_ellipse
################################################################################
#
#
#
#### scan the maxima                                                                    !!!
#def scan_for_maxima(data_in, ellipse):
#    
#    x_c = int(ellipse[0][0])
#    y_c = int(ellipse[0][1])
#    
##    dx = np.abs(x_c - int(ellipse[1][0]))
##    dy = np.abs(y_c - int(ellipse[1][1]))
#    
#    line_1_x = []
#    line_1_y = []
#
#    line_2_x = []
#    line_2_y = []
#    
#    for i in range(len(data_in)):
#        row_1 = data_in[i][:y_c]
#        row_2 = data_in[i][y_c+1:]
#
#        index_max_1 = np.argmax(row_1)
#        index_max_2 = np.argmax(row_2)
#        
#        if i > 50 and i < 1010:
#            if index_max_1 > 170:
#                line_1_x.append(i)
#                line_1_y.append(index_max_1)
#                
#        if i > 50 and i < 1010:
#            if index_max_2 < 170:
#                line_2_x.append(i)
#                line_2_y.append(index_max_2 + y_c + 1)
#    
#    return [line_1_x, line_1_y], [line_2_x, line_2_y]
#
#
#### scan the maxima                                                                    !!!
#def get_lin_fit(x_data, y_data, p0):
#
#    x_values = np.array(x_data)    
#    y_values = np.array(y_data)
#
#    fitfunc = lambda p, x: p[0]*x + p[1]
#    errfunc = lambda p, x, y: fitfunc(p, x) - y
#    
#    p1, success = optimize.leastsq(errfunc, p0[:], args=(x_values,y_values))
#    m, b, r_value, p_value, std_err = stats.linregress(x_values, y_values)
#             
#    return p1, std_err
#
#
#### scan the maxima                                                                    !!!
#def get_fit_to_plot(x_data,fit_res):
#    
#    y_fit = []
#    
#    for i in range(len(x_data)):
#        value = fit_res[0]*x_data[i] + fit_res[1]
#        y_fit.append(value)
#    
#    return x_data, y_fit
#
#
#
#
#
#
#### get indices of the two maxima in the projection ###########################
#def get_ri_Be(data_in, center):
#    
#    c = int(center)
#    data_1 = data_in[:c]
#    data_2 = data_in[c:]
#    
#    index_max_1 = data_1.index(max(data_1))
#    index_max_2 = data_2.index(max(data_2)) + c - 1
#           
#    return index_max_1, index_max_2
################################################################################  
#
#
#
#### get the start and end indices of the inner ion shell depending on mass and
#### inner radius of the outer shell ########################################### 
#def get_ro_H2(ri_in_1, ri_in_2,  m_larger, m_smaller):
#    
#    ### center of the inner shell
#    c = (ri_in_1 + ri_in_2)/2.0
#    
#    ### inner radius of the outer shell
#    ri = (np.abs(c - ri_in_1) + np.abs(c - ri_in_2))/2.0
#    
#    ### outer radius of the inner shell
#    ro = np.sqrt(m_smaller/m_larger) * ri
#    
#    ### the indices
#    ro_1 = int(c - ro)
#    ro_2 = int(c + ro)
#       
#    return ro_1, ro_2
################################################################################  
#    
#
#
#### get the volumina occupied by the Be+ and H2+ ions #########################
#def get_volumina(ellipse, ri_be_1_in, ri_be_2_in, ro_h2_1_in, ro_h2_2_in, cam_m_per_pixel):
#    
#    ### volume ellipse in m^3
#    ell_semi_minor_axis = ellipse[1][0]/2.0 * cam_m_per_pixel
#    ell_semi_major_axis = ellipse[1][1]/2.0 * cam_m_per_pixel
#    
#    ell_volume = 4.0/3.0 * np.pi * ell_semi_minor_axis**2 * ell_semi_major_axis
#    
#    ### approximate volume cylinder not occupied by Be+
#    r_be = np.abs(ri_be_2_in-ri_be_1_in)/2.0 * cam_m_per_pixel
#    
#    be_cylinder_volume = np.pi * r_be**2 * 2*ell_semi_major_axis
#    
#    ### volume occupied by Be+
#    volume_be = ell_volume - be_cylinder_volume
#
#
#    ### approximate volume cylinder occupied by H2+
#    r_h2 = np.abs(ro_h2_2_in-ro_h2_1_in)/2.0 * cam_m_per_pixel
#    
#    volume_h2 = np.pi * r_h2**2 * 2*ell_semi_major_axis
#
#    
#    return volume_be, volume_h2
################################################################################  
#    
#
#    
#
#
#### to cross check - determine the ratio of the secular frequencies from the ##
#### shape of the ion crystal ##################################################
#def get_sec_frequ_from_crystal_shape(ellipse):
#    
#    ### minor and major axis
#    ell_semi_minor_axis = ellipse[1][0]/2.0
#    ell_semi_major_axis = ellipse[1][1]/2.0
#    
#    alpha = ell_semi_major_axis/ell_semi_minor_axis
#    
#    ratio = -2.0 * (np.arcsin(np.sqrt(1-1/alpha**2)) - alpha * np.sqrt(1-1/alpha**2)) / (np.arcsin(np.sqrt(1-1/alpha**2)) - 1/alpha * np.sqrt(1-1/alpha**2))
#    
#    return ratio
################################################################################
    









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