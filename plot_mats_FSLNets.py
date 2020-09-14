# the motivation behind this script was to tackle a problem in FSLNets
# the connectivity matrices are generated using imagesc
# it always converts the figure to a bitmap even if you wanted svg (obviusly an internal problem)
# pcolor function obviusly does the same, and figures can be saved as svg
# only ptoblem, in matlab, pcolor omits a column and a row
# I went to python, same story
# plt.imshow -> NO svg
# but, pcolor does not omit anything and retruns identical results, only pproblem the y-axis is flipped
# I compred various results and plt.pcolor works well
# the missing link was to export the the matrices that are plotted from mat to python

# I added the following additions to FSLNets scripts:
# >>>> nets_groupmean.m:
#
#      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#      fname = sprintf('/media/amr/Amr_4TB/Dropbox/thesis/resting/FSLNets_pics/%s_Znetd.mat', inputname(1)); %%%added by amr to name the variable for plotting after input
#      save(fname,'Znetd')  %%%added by amr to name the variable for plotting after input
#      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# >>>> nets_hierarchy.m:
#  fname = sprintf('/media/amr/Amr_4TB/Dropbox/thesis/resting/FSLNets_pics/%s_%s_grot.mat', inputname(1), inputname(2)); %%%added by amr to name the variable for plotting after input
#  save(fname,'grot')  %%%added by amr to name the variable for plotting after input


# Now the script import the matrices and plots them

def plot_pcolor_map(matrix, vmin, vmax, dir):
    import matplotlib.pyplot as plt
    from scipy.io import loadmat
    import ntpath  # get the file name from abs path to use it to name the maps

    mat = loadmat(matrix)
    # the loaded mat from matlab is in the format of dict
    # we need to index it with name of the mat
    # but you cannot index dict_keys, so we retrun them as a list and take the first element
    name_mat = list(mat.keys())

    mat = mat[name_mat[3]]
    filename = ntpath.basename(matrix)

    plt.pcolor(mat, vmin=vmin, vmax=vmax, cmap='coolwarm')
    plt.gca().invert_yaxis()  # the y-axis is flipped, I flip it back
    plt.colorbar()
    plt.savefig('{0}/{1}.svg'.format(dir, filename), format='svg')
    plt.clf()  # close the figure before plotting new, this way colorbars do not accumulate


# ======================================================================================================
# plot the one-sample t-test of connectivity

# the output from FSLNets is:
# nets_groupmean.m:
# netmats_F_Znetd.mat      netmats_P_Znetd.mat      netmats_rP_Znetd.mat
dir = '/Users/amr/Dropbox/thesis/resting/FSLNets_pics'
plot_pcolor_map('/Users/amr/Dropbox/thesis/resting/FSLNets_pics/netmats_F_Znetd.mat', -10, 10, dir)
plot_pcolor_map('/Users/amr/Dropbox/thesis/resting/FSLNets_pics/netmats_P_Znetd.mat', -10, 10, dir)
plot_pcolor_map('/Users/amr/Dropbox/thesis/resting/FSLNets_pics/netmats_rP_Znetd.mat', -10, 10, dir)

# nets_hierarchy.m:
# Znet_F_Znet_P_grot.mat   Znet_F_Znet_rP_grot.mat  Znet_P_Znet_rP_grot.mat
plot_pcolor_map('/Users/amr/Dropbox/thesis/resting/FSLNets_pics/Znet_F_Znet_P_grot.mat', -1, 1, dir)
plot_pcolor_map('/Users/amr/Dropbox/thesis/resting/FSLNets_pics/Znet_F_Znet_rP_grot.mat', -1, 1, dir)
plot_pcolor_map('/Users/amr/Dropbox/thesis/resting/FSLNets_pics/Znet_P_Znet_rP_grot.mat', -1, 1, dir)
