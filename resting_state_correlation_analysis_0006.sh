#!/bin/bash
#perform correlation analysis between behavior metrics and ICA maps of the resting state data
# first copy the metrics from the ouput of the behavior ouput to here
# I am suspecting that a lot of the metrics are linear combinations of the others


# Copy the file that contains all the begavior from the VBM stat directory:
# They are well-organized and demeaned, so it is more convenient
# OF: /media/amr/Amr_4TB/Work/October_Acquistion/VBM/VBM_corr_designs/open_field_gp_names.csv
# EPM: /media/amr/Amr_4TB/Work/October_Acquistion/VBM/VBM_corr_designs/plus_maze_gp_names.csv

# animals: 271, 272 are omitted, hence the difference
# for each column, I subtract the mean and create design from each one of them
# in those cases the DOF will be 30-2 (rows - columns(contrasts)) = 28

mkdir /media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr
mkdir /media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs

cp \
/media/amr/Amr_4TB/Work/October_Acquistion/VBM/VBM_corr_designs/open_field_gp_names.csv \
 /media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs

cp \
/media/amr/Amr_4TB/Work/October_Acquistion/VBM/VBM_corr_designs/plus_maze_gp_names.csv \
 /media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs

# I edited the CSV files manually to remove the extra subjects
# I did the designs manually, by calling Glm and fill in the data from the CSV files

# Copy the dr_stage2 maps of the 20 dim for the correlation analysis
mkdir /media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim


cp \
/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_gp_ICA+DR_workingdir/melodic_workflow/_dim_20/dual_regression/output/dr_stage2_ic00??.nii.gz \
/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim

# decompress them to make palm's life easy

gunzip -d /media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/*.nii.gz
