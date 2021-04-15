# plot the correlation between the amplitude and the behavior
# since only amplitude was correlated with behavioral markaers
# reminder from the matlab script, the behaviorla markers with significant values were:
# TODO: compare the final plots between mac and linux
# TODO: modify the correlation.m script to save the netmats_A
# EPM_open_to_close_ratio_p_corrected_A
# EPM_time_in_closed_arms_p_corrected_A
# EPM_time_in_closed_arms_percent_p_corrected_A
# EPM_time_in_opened_arms_p_corrected_A
# EPM_time_in_opened_arms_percent_p_corrected_A

import numpy as np
import matplotlib.pyplot as plt
import nipype.interfaces.fsl as fsl
import ntpath
import sys
import matplotlib
import os
from scipy.io import loadmat


def plot_amplitude_correlation(amp_mat_path, netmats_A_path):
    # 1- get the amplitudes
    # load the matlab mat to python
    mat = loadmat(amp_mat_path)
    # extract only the array
    mat_ndarray = mat['p_corrected_A']
    # get the index of the significant element in the matrix
    loc = np.nonzero(mat_ndarray > 0.949)
    # convert the ndarray containing the column location to a list of one element
    index_sig_col = loc[1].astype(list)
    # load the netmats_A matrix
    netmats_A = loadmat(netmats_A_path)
    netmats_A = netmats['netmats_A']
    # use the col index to get the amplitudes of the 30 subjects from the netmats
    amplitudes = netmats_A[:, index_sig_col]
