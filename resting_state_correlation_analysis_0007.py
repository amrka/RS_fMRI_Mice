# running correlation analysis for OF and EPM using different designs
# each design represents one varible
# we have 30 animals in rs analysis - two contrasts, +ve and -ve correlation
# hence we have 28 dof, degrees of freedom
from nipype import config
cfg = dict(execution={'remove_unnecessary_outputs': False})
config.update_config(cfg)
#-------------------------------------------------------------------------------------
import nipype.interfaces.fsl as fsl
import nipype.interfaces.afni as afni
import nipype.interfaces.ants as ants
import nipype.interfaces.spm as spm
import nipype.interfaces.utility as utility
from nipype.interfaces.utility import IdentityInterface, Function
from os.path import join as opj
from nipype.interfaces.io import SelectFiles, DataSink
from nipype.pipeline.engine import Workflow, Node, MapNode
import numpy as np
import matplotlib.pyplot as plt
#-------------------------------------------------------------------------------------
experiment_dir = '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/'


map_list=  ['dr_stage2_20_dim']

output_dir  = 'resting_state_correlation_analysis_outputdir'
working_dir = 'resting_state_correlation_analysis_workingdir'

resting_state_corr = Workflow (name = 'resting_state_correlation_analysis')
resting_state_corr.base_dir = opj(experiment_dir, working_dir)
#-----------------------------------------------------------------------------------------------------
infosource = Node(IdentityInterface(fields=['map_id']),
                  name="infosource")
infosource.iterables = [('map_id', map_list)]

#-----------------------------------------------------------------------------------------------------
templates = {

        'ICA_mask'  : '{map_id}/anat_template_enhanced_mask_2.nii'
 }
selectfiles = Node(SelectFiles(templates,
                               base_directory=experiment_dir),
                   name="selectfiles")

#-----------------------------------------------------------------------------------------------------
datasink = Node(DataSink(), name = 'datasink')
datasink.inputs.container = output_dir
datasink.inputs.base_directory = experiment_dir

substitutions = [('_map_id_', ''),
('_contrast_..home..in..aeed..Work..October_Acquistion..VBM..VBM_corr_designs..', ''),
('design_..home..in..aeed..Work..October_Acquistion..VBM..VBM_corr_designs..', ''),
]

datasink.inputs.substitutions = substitutions


#-----------------------------------------------------------------------------------------------------
# designs and contrasts done manullay

designs = [
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_open_to_close_ratio.mat',
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_time_in_center.mat',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_time_in_center_percent.mat',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_time_in_closed_arms.mat',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_time_in_closed_arms_percent.mat',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_time_in_opened_arms.mat',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_time_in_opened_arms_percent.mat',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_total_distance.mat',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_velocity.mat',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/OF_center_corners_ratio.mat',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/OF_percent_in_center.mat',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/OF_percent_in_corners.mat',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/OF_sec_in_center.mat',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/OF_total_distance.mat',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/OF_total_time_in_corners.mat',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/OF_velocity.mat'
]

contrasts = [
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_open_to_close_ratio.con',
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_time_in_center.con',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_time_in_center_percent.con',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_time_in_closed_arms.con',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_time_in_closed_arms_percent.con',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_time_in_opened_arms.con',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_time_in_opened_arms_percent.con',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_total_distance.con',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_velocity.con',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/OF_center_corners_ratio.con',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/OF_percent_in_center.con',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/OF_percent_in_corners.con',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/OF_sec_in_center.con',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/OF_total_distance.con',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/OF_total_time_in_corners.con',
# '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/OF_velocity.con'
]


#-----------------------------------------------------------------------------------------------------
def palm_corr(in_file, mask, design, contrast):
    import os
    from glob import glob
    from nipype.interfaces.base import CommandLine


    cmd = ("palm \
    -i /media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0000.nii \
    -i /media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0001.nii \
    -i /media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0002.nii \
    -i /media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0003.nii \
    -i /media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0004.nii \
    -i /media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0005.nii \
    -i /media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0006.nii \
    -i /media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0007.nii \
    -i /media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0008.nii \
    -i /media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0009.nii \
    -i /media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0010.nii \
    -i /media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0011.nii \
    -i /media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0012.nii \
    -i /media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0013.nii \
    -i /media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0014.nii \
    -i /media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0015.nii \
    -i /media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0016.nii \
    -i /media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0017.nii \
    -i /media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0018.nii \
    -i /media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0019.nii \
    -m {mask} \
    -d {design} -t {contrast} \
    -T -noniiclass -n 10 -corrcon -corrmod -save1-p -o palm_corr_vbm")
    # start with 1000 and if you find something interesting, go to 10000


    cl = CommandLine(cmd.format(in_file=in_file, mask=mask, design=design, contrast=contrast ))
    cl.run()
    # tstat1 = os.path.abspath('palm_corr_vbm_vox_tstat_c1.nii.gz')
    # tstat2 = os.path.abspath('palm_corr_vbm_vox_tstat_c2.nii.gz')
    # P_value1 = os.path.abspath('palm_corr_vbm_tfce_tstat_fwep_c1.nii.gz')
    # P_value2 = os.path.abspath('palm_corr_vbm_tfce_tstat_fwep_c2.nii.gz')

    return tstat1, tstat2#, P_value1, P_value2

palm_corr = Node(name = 'palm_corr',
                 interface = Function(input_names = ['in_file', 'mask', 'design', 'contrast'],
                                        # output_names = ['tstat1', 'tstat2', 'P_value1', 'P_value2'],
                                      function = palm_corr))


palm_corr.iterables = [("design", designs),("contrast", contrasts)]
palm_corr.synchronize = True # synchronize here serves to make sure design and contrast are used in pairs
# Not using all the possible permuatations
#-----------------------------------------------------------------------------------------------------
# use the tstat maps to calculate r-pearson correlation coeeficient
# >>> fslmaths tstat.nii.gz -sqr tstat2.nii.gz
# >>> fslmaths tstat.nii.gz -abs -div tstat.nii.gz sign.nii.gz
# >>> fslmaths tstat2.nii.gz -add DF denominator.nii.gz
# >>> fslmaths tstat2.nii.gz -div denominator.nii.gz -sqrt -mul sign.nii.gz correlation.nii.gz
square1 = Node(fsl.UnaryMaths(), name='square1')
square1.inputs.operation = 'sqr'
square1.inputs.out_file = 'tstat1_squared.nii.gz'

sign_t1 = Node(fsl.ImageMaths(), name='sign_t1')
sign_t1.inputs.op_string = '-abs -div'
sign_t1.inputs.out_file = 'sign_tstat1.nii.gz'

add_df1 = Node(fsl.BinaryMaths(), name='add_df1')
add_df1.inputs.operation = 'add'
add_df1.inputs.operand_value = 28 #30 animals-2contrast = 28 dof
add_df1.inputs.out_file = 'denominator_tstat1.nii.gz'

div_by_denom1 = Node(fsl.BinaryMaths(), name='div_by_denom1')
div_by_denom1.inputs.operation = 'div'
div_by_denom1.inputs.out_file = 'divided_by_denominator.nii.gz'


# the correlation coefficient was tested against using the flag -pearson
# as well as aginst using just the bash commands written by anderson (see above)
# the results are 100% exactly the same
create_corr1 = Node(fsl.ImageMaths(), name='create_corr1')
create_corr1.inputs.op_string = '-sqrt -mul'
create_corr1.inputs.out_file = 'corr_coef_r1.nii.gz'
#-----------------------------------------------------------------------------------------------------
# same thing with tstat2 to get r2
square2 = Node(fsl.UnaryMaths(), name='square2')
square2.inputs.operation = 'sqr'
square2.inputs.out_file = 'tstat2_squared.nii.gz'

sign_t2 = Node(fsl.ImageMaths(), name='sign_t2')
sign_t2.inputs.op_string = '-abs -div'
sign_t2.inputs.out_file = 'sign_tstat2.nii.gz'

add_df2 = Node(fsl.BinaryMaths(), name='add_df2')
add_df2.inputs.operation = 'add'
add_df2.inputs.operand_value = 28 #30 animals-2contrast = 28 dof
add_df2.inputs.out_file = 'denominator_tstat2.nii.gz'

div_by_denom2 = Node(fsl.BinaryMaths(), name='div_by_denom2')
div_by_denom2.inputs.operation = 'div'
div_by_denom2.inputs.out_file = 'divided_by_denominator.nii.gz'

create_corr2 = Node(fsl.ImageMaths(), name='create_corr2')
create_corr2.inputs.op_string = '-sqrt -mul'
create_corr2.inputs.out_file = 'corr_coef_r2.nii.gz'


#-----------------------------------------------------------------------------------------------------
VBM_corr.connect ([

      (infosource, selectfiles,[('map_id','map_id')]),

      # (selectfiles, palm_corr, [('VBM','in_file')]),
      (selectfiles, palm_corr, [('VBM_mask','mask')]),
      #
      # (palm_corr, datasink, [('tstat1','tstat1')]),
      # (palm_corr, datasink, [('tstat2','tstat2')]),
      #
      # (palm_corr, datasink, [('P_value1','P_value1')]),
      # (palm_corr, datasink, [('P_value2','P_value2')]),
#==================================r1==============================================
      # (palm_corr, square1, [('tstat1','in_file')]),
      #
      # (palm_corr, sign_t1, [('tstat1','in_file')]),
      # (palm_corr, sign_t1, [('tstat1','in_file2')]),
      #
      # (square1, add_df1, [('out_file','in_file')]),
      #
      # (square1, div_by_denom1, [('out_file','in_file')]),
      # (add_df1, div_by_denom1, [('out_file','operand_file')]),
      #
      # (div_by_denom1, create_corr1, [('out_file','in_file')]),
      # (sign_t1, create_corr1, [('out_file','in_file2')]),
      #
      # (create_corr1, datasink, [('out_file','corr_coef_r1')]),
#==================================r2==============================================
      # (palm_corr, square2, [('tstat2','in_file')]),
      #
      # (palm_corr, sign_t2, [('tstat2','in_file')]),
      # (palm_corr, sign_t2, [('tstat2','in_file2')]),
      #
      # (square2, add_df2, [('out_file','in_file')]),
      #
      # (square2, div_by_denom2, [('out_file','in_file')]),
      # (add_df2, div_by_denom2, [('out_file','operand_file')]),
      #
      # (div_by_denom2, create_corr2, [('out_file','in_file')]),
      # (sign_t2, create_corr2, [('out_file','in_file2')]),
      #
      # (create_corr2, datasink, [('out_file','corr_coef_r2')]),
  ])


VBM_corr.write_graph(graph2use='colored', format='svg', simple_form=True)
# VBM_corr.run(plugin='SLURM', plugin_args={'dont_resubmit_completed_jobs': True,'max_jobs':50, 'sbatch_args':'--mem=16G'})
# plugin_args={'sbatch_args': '--time=24:00:00 -N1 -c2 --mem=40G','max_jobs':200}
VBM_corr.run('MultiProc', plugin_args={'n_procs': 8})
