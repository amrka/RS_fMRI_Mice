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


def plot_amplitude_correlation(amp_mat_path, netmats_A_path, design_mat_path):
    # 1- get the amplitudes
    # load the matlab mat to python
    mat = loadmat(amp_mat_path)
    # extract only the array
    mat_ndarray = mat['p_corrected_A']
    # get the index of the significant element in the matrix
    loc = np.nonzero(mat_ndarray > 0.949)
    # get the exact p_values to use it later
    p_value = mat_ndarray[mat_ndarray > 0.949]
    # convert the ndarray containing the column location to a list of one element
    index_sig_col = loc[1].astype(list)
    # load the netmats_A matrix
    netmats_A = loadmat(netmats_A_path)
    netmats_A = netmats['netmats_A']
    # use the col index to get the amplitudes of the 30 subjects from the netmats
    amplitudes = netmats_A[:, index_sig_col]

    # 2- get the behavioral values from design matrix
    mat_basename_no_ext = ntpath.basename(design_mat_path)[:-4]
    fh = open(design_mat_path, 'r')
    lines = fh.readlines()
    fh.close()
    behav = []
    i = 5
    for item in lines:
        while i < len(lines):
            behav.append(float(lines[i][13:-2]))
            i = i + 1

    # sanity check
    print("length of amplitudes_values -> {0}".format(len(amplitudes)))
    print("length of behav_values -> {0}".format(len(behav)))
    if len(amplitudes) != len(behav):
        sys.error('######ERROR####')

    # 3- do the actual plotting
    # the regression line
    coef = np.polyfit(amplitudes, behav, 1)
    poly1d_fn = np.poly1d(coef)

    # get the correlation coeeficient
    # round to 4 digits after the decimal point
    correlation_coef = round(np.corrcoef(amplitudes, behav)[0, 1], 5)

    plt.rcParams['font.family'] = 'Arial'

    ax = plt.axes()
    ax.spines['bottom'].set_color('#ffffffff')
    ax.spines['top'].set_color('#ffffffff')
    ax.spines['right'].set_color('#ffffffff')
    ax.spines['left'].set_color('#ffffffff')
    ax.tick_params(axis='x', colors='#ffffffff')
    ax.tick_params(axis='y', colors='#ffffffff')

    plt.xticks(fontsize=14, rotation=45, color='#ffffffff')
    plt.yticks(fontsize=14, color='#ffffffff')
    plt.scatter(amplitudes[:16], behav[:16], marker='o', color='#e41a1c')
    plt.scatter(amplitudes[16:], behav[16:], marker='<', color='#377eb8')
    plt.ylabel("{0}".format(mat_basename_no_ext), fontsize=18, fontname='Arial', color='#ffffffff')
    plt.plot(amplitudes, poly1d_fn(amplitudes), color='#ffffffff')  # plot the regression line
    # type the coef on the graph, first two arguments the coordinates of the text (top left corner)
    plt.text(min(amplitudes), max(behav), "r $= {0}$".format(
        correlation_coef), fontname="Arial", style='italic', fontsize=14, color='#ffffffff')

    plt.savefig("/Users/amr/Dropbox/thesis/diffusion/DTI_corr/{0}_{1}.svg".format(
        img_basename_no_ext, mat_basename_no_ext), format='svg')
    plt.close()

    os.remove(ts)  # delete the file of the voxel values as it is no longer needed
    os.remove('stat_result.json')
