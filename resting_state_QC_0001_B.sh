#!/bin/bash

#moving some important files to look at them seperately

cd /Volumes/Amr_1TB/resting_state
mkdir -p QC/{brain_ext,anat_eroded,coreg,reg}


cd /Volumes/Amr_1TB/resting_state/resting_state_preproc_workingdir/resting_fmri_preproc

#================================================================================================================================================================================
#brain extracted	
imcp \
/Volumes/Amr_1TB/resting_state/resting_state_preproc_workingdir/resting_fmri_preproc/_subject_id_???/brain_extraction_roi/rs_fMRI_???_roi_masked.nii.gz \
/Volumes/Amr_1TB/resting_state/QC/brain_ext/

#create an image to facilitate inspection
cd /Volumes/Amr_1TB/resting_state/QC/brain_ext/
for img in *;do
	slicer $img -A 800 ${img}.png
done



#================================================================================================================================================================================
#anat_eroded
imcp \
/Volumes/Amr_1TB/resting_state/resting_state_preproc_workingdir/resting_fmri_preproc/_subject_id_???/erode_anatomical_image/Anat_Bet_???_corrected_ero.nii.gz \
/Volumes/Amr_1TB/resting_state/QC/anat_eroded/


#create an image to facilitate inspection
cd /Volumes/Amr_1TB/resting_state/QC/anat_eroded/
for img in *;do
	slicer $img -A 800 ${img}.png
done



#================================================================================================================================================================================
#coregistered	
for img in /Volumes/Amr_1TB/resting_state/resting_state_preproc_workingdir/resting_fmri_preproc/_subject_id_???/coregistration/transform_Warped.nii.gz;do
	subj_no=${img:97:3}
	imcp $img \
	/Volumes/Amr_1TB/resting_state/QC/coreg/coreg_${subj_no}
done



#================================================================================================================================================================================
#registration	
for img in /Volumes/Amr_1TB/resting_state/resting_state_preproc_workingdir/resting_fmri_preproc/_subject_id_???/reg_T1_2_temp/transform_Warped.nii.gz;do
	subj_no=${img:97:3}
	imcp $img \
	/Volumes/Amr_1TB/resting_state/QC/reg/reg_2_temp_${subj_no}

	slicer  /Volumes/Amr_1TB/anat_temp_new/anat_temp_enhanced_3.nii.gz $img -A 800 /Volumes/Amr_1TB/resting_state/QC/reg/${subj_no}.png
done





