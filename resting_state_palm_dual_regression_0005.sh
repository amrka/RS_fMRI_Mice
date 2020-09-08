#!/bin/bash

#create a directory for palm_dual_regression

mkdir -p /Volumes/Amr_1TB/resting_state/palm_dual_regression/{dim_10,dim_15,dim_20,dim_25}


#-----------------------------------------------------------------------------------------------------
#dim_20
dim=20
for file in /Volumes/Amr_1TB/resting_state/resting_state_gp_ICA+DR_workingdir/melodic_workflow/_dim_${dim}/dual_regression/output/dr_stage2_ic00??.nii.gz;do
	imcp ${file} \
	/Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/
done

#uncompress to use with palm
gunzip /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/*.nii.gz

 # that is the correct mask
palm \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0000.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0001.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0002.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0003.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0004.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0005.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0006.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0007.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0008.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0009.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0010.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0011.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0012.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0013.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0014.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0015.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0016.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0017.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0018.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0019.nii \
-m /Volumes/Amr_1TB/anat_temp_new/anat_template_enhanced_mask_2.nii.gz \
-d /Volumes/Amr_1TB/resting_state/Design_october_Acquistion_dual_regression.mat \
-t /Volumes/Amr_1TB/resting_state/Design_october_Acquistion_dual_regression.con \
-n 5000 \
-corrmod \
-corrcon \
-noniiclass \
-save1-p \
-T \
-o /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dim_${dim}_palm_stage3_

#--------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------
#dim_15 I copy the code becasue I need to determine the input -i, using wildcards does not work
dim=15
for file in /Volumes/Amr_1TB/resting_state/resting_state_gp_ICA+DR_workingdir/melodic_workflow/_dim_${dim}/dual_regression/output/dr_stage2_ic00??.nii.gz;do
	imcp ${file} \
	/Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/
done

#uncompress to use with palm
gunzip /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/*.nii.gz

palm \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0000.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0001.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0002.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0003.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0004.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0005.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0006.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0007.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0008.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0009.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0010.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0011.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0012.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0013.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0014.nii  \
-m /Volumes/Amr_1TB/anat_temp_new/anat_template_enhanced_mask_2.nii.gz \
-d /Volumes/Amr_1TB/resting_state/Design_october_Acquistion_dual_regression.mat \
-t /Volumes/Amr_1TB/resting_state/Design_october_Acquistion_dual_regression.con \
-n 5000 \
-corrmod \
-corrcon \
-noniiclass \
-save1-p \
-T \
-o /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dim_${dim}_palm_stage3_
#-----------------------------------------------------------------------------------------------------
#dim_15 I copy the code becasue I need to determine the input -i, using wildcards does not work
dim=25
for file in /Volumes/Amr_1TB/resting_state/resting_state_gp_ICA+DR_workingdir/melodic_workflow/_dim_${dim}/dual_regression/output/dr_stage2_ic00??.nii.gz;do
	imcp ${file} \
	/Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/
done

#uncompress to use with palm
gunzip /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/*.nii.gz

palm \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0000.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0001.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0002.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0003.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0004.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0005.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0006.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0007.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0008.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0009.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0010.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0011.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0012.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0013.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0014.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0015.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0016.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0017.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0018.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0019.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0020.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0021.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0022.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0023.nii  \
-i /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dr_stage2_ic0024.nii  \
-m /Volumes/Amr_1TB/anat_temp_new/anat_template_enhanced_mask_2.nii.gz \
-d /Volumes/Amr_1TB/resting_state/Design_october_Acquistion_dual_regression.mat \
-t /Volumes/Amr_1TB/resting_state/Design_october_Acquistion_dual_regression.con \
-n 5000 \
-corrmod \
-corrcon \
-noniiclass \
-save1-p \
-T \
-o /Volumes/Amr_1TB/resting_state/palm_dual_regression/dim_${dim}/dim_${dim}_palm_stage3_
