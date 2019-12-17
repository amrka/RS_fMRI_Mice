#!/bin/bash
#move the filtered 4D images to be used for group ICA and later for dual regression

mkdir /Volumes/Amr_1TB/resting_state/resting_state_gp_ICA_DR


cd /Volumes/Amr_1TB/resting_state/resting_state_metaflow_outputdir/func_filt_temp_space

for subj in *;do
	imcp ${subj}/*.nii.gz /Volumes/Amr_1TB/resting_state/resting_state_gp_ICA_DR/rsfMRI_filtered_${subj}
done




python3 /Users/amr/Dropbox/SCRIPTS/change_files_to_contain_gp_name.py /Volumes/Amr_1TB/resting_state/resting_state_gp_ICA_DR -10 -7

ls /Volumes/Amr_1TB/resting_state/resting_state_gp_ICA_DR/*.nii.gz >> /Volumes/Amr_1TB/resting_state/resting_state_gp_ICA_DR/melodic_list_october_acquistions.txt


#then you create the design