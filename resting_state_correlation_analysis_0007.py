# running correlation analysis for OF and EPM using different designs
# each design represents one varible
# we have 30 animals in rs analysis - two contrasts, +ve and -ve correlation
# hence we have 28 dof, degrees of freedom
import matplotlib.pyplot as plt
import numpy as np
from nipype.pipeline.engine import Workflow, Node, MapNode
from nipype.interfaces.io import SelectFiles, DataSink
from os.path import join as opj
from nipype.interfaces.utility import IdentityInterface, Function
import nipype.interfaces.utility as utility
import nipype.interfaces.spm as spm
import nipype.interfaces.ants as ants
import nipype.interfaces.afni as afni
import nipype.interfaces.fsl as fsl
from nipype import config
cfg = dict(execution={'remove_unnecessary_outputs': False})
config.update_config(cfg)
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
experiment_dir = '/home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/'


design_list = ['EPM_open_to_close_ratio.mat',
               'EPM_time_in_center.mat',
               'EPM_time_in_center_percent.mat',
               'EPM_time_in_closed_arms.mat',
               'EPM_time_in_closed_arms_percent.mat',
               'EPM_time_in_opened_arms.mat',
               'EPM_time_in_opened_arms_percent.mat',
               'EPM_total_distance.mat',
               'EPM_velocity.mat',
               'OF_percent_in_center.mat',
               'OF_percent_in_corners.mat',
               'OF_sec_in_center.mat',
               'OF_total_distance.mat',
               'OF_total_time_in_corners.mat',
               'OF_velocity.mat',
               ]

contrast_list = ['EPM_open_to_close_ratio.con',
                 'EPM_time_in_center.con',
                 'EPM_time_in_center_percent.con',
                 'EPM_time_in_closed_arms.con',
                 'EPM_time_in_closed_arms_percent.con',
                 'EPM_time_in_opened_arms.con',
                 'EPM_time_in_opened_arms_percent.con',
                 'EPM_total_distance.con',
                 'EPM_velocity.con',
                 'OF_percent_in_center.con',
                 'OF_percent_in_corners.con',
                 'OF_sec_in_center.con',
                 'OF_total_distance.con',
                 'OF_total_time_in_corners.con',
                 'OF_velocity.con',
                 ]

output_dir = 'resting_state_correlation_analysis_outputdir'
working_dir = 'resting_state_correlation_analysis_workingdir'

resting_state_corr = Workflow(name='resting_state_correlation_analysis')
resting_state_corr.base_dir = opj(experiment_dir, working_dir)
# -----------------------------------------------------------------------------------------------------
infosource = Node(IdentityInterface(fields=['design_id', 'contrast_id']),
                  name="infosource")
infosource.iterables = [('design_id', design_list), ('contrast_id', contrast_list)]
infosource.synchronize = True  # to pick them in pairs, the design and the contrast

# -----------------------------------------------------------------------------------------------------
templates = {

    'design': 'resting_state_corr_designs/{design_id}',
    'contrast': 'resting_state_corr_designs/{contrast_id}'
}
selectfiles = Node(SelectFiles(templates,
                               base_directory=experiment_dir),
                   name="selectfiles")

# -----------------------------------------------------------------------------------------------------
datasink = Node(DataSink(), name='datasink')
datasink.inputs.container = output_dir
datasink.inputs.base_directory = experiment_dir

substitutions = [('_contrast_id_', ''), ('_design_id_', ''), ('.mat', ''),
                 ('EPM_open_to_close_ratio.con', ''),
                 ('EPM_time_in_center.con', ''),
                 ('EPM_time_in_center_percent.con', ''),
                 ('EPM_time_in_closed_arms.con', ''),
                 ('EPM_time_in_closed_arms_percent.con', ''),
                 ('EPM_time_in_opened_arms.con', ''),
                 ('EPM_time_in_opened_arms_percent.con', ''),
                 ('EPM_total_distance.con', ''),
                 ('EPM_velocity.con', ''),
                 ('OF_percent_in_center.con', ''),
                 ('OF_percent_in_corners.con', ''),
                 ('OF_sec_in_center.con', ''),
                 ('OF_total_distance.con', ''),
                 ('OF_total_time_in_corners.con', ''),
                 ('OF_velocity.con', '')]

datasink.inputs.substitutions = substitutions


# -----------------------------------------------------------------------------------------------------
def palm_corr(design, contrast):
    import os
    import glob
    from nipype.interfaces.base import CommandLine

 # that is the correct mask
    cmd = ("palm \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0000.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0001.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0002.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0003.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0004.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0005.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0006.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0007.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0008.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0009.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0010.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0011.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0012.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0013.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0014.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0015.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0016.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0017.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0018.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0019.nii \
    -m /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/anat_template_enhanced_mask_2.nii \
    -d {design} -t {contrast} \
    -T -noniiclass -n 5000 -corrcon -corrmod -save1-p -nouncorrected -o palm_corr_rs")
    # start with 5000 like the rest of resting state

    cl = CommandLine(cmd.format(design=design, contrast=contrast))
    cl.run()

    P_values = []
    for file in glob.glob(os.path.abspath('palm_corr_rs_tfce_tstat_mfwep_*')):
        P_values.append(file)
    return P_values


palm_corr = Node(name='palm_corr',
                 interface=Function(input_names=['design', 'contrast'],
                                    output_names=['P_values'],
                                    function=palm_corr))

# -----------------------------------------------------------------------------------------------------
# instead of calculating r from tstat like in VBM and DTI, I used -pearson flag
# there is tstats for each module, it would have been so much work to them with nodes


def palm_corr_pearson(design, contrast):
    import os
    import glob
    from nipype.interfaces.base import CommandLine

    cmd = ("palm \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0000.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0001.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0002.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0003.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0004.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0005.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0006.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0007.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0008.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0009.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0010.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0011.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0012.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0013.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0014.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0015.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0016.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0017.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0018.nii \
    -i /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/dr_stage2_ic0019.nii \
    -m /home/in/aeed/Work/October_Acquistion/resting_state/resting_state_corr/dr_stage2_20_dim/anat_template_enhanced_mask_2.nii \
    -d {design} -t {contrast} \
    -T -noniiclass -n 3 -pearson -corrcon -corrmod -save1-p -nouncorrected -o palm_corr_pearson")
    # we do with 3 (or 1 or 2) as I am looking for correlation coefficient, I do not want P_values
    # Hence, no need for permutations

    cl = CommandLine(cmd.format(design=design, contrast=contrast))
    cl.run()

    corr_coefs = []
    for file in glob.glob(os.path.abspath('palm_corr_pearson_vox_rstat_m??_c?.nii.gz')):
        corr_coefs.append(file)
# the files are not zero padded, for example instead of *_m01_*, it is *_m1_*
# using an asterisk instead of ??, copies other files sych as mcfwep
    for file in glob.glob(os.path.abspath('palm_corr_pearson_vox_rstat_m?_c?.nii.gz')):
        corr_coefs.append(file)

    return corr_coefs


palm_corr_pearson = Node(name='palm_corr_pearson',
                         interface=Function(input_names=['design', 'contrast'],
                                            output_names=['corr_coefs'],
                                            function=palm_corr_pearson))
# -----------------------------------------------------------------------------------------------------
resting_state_corr.connect([

    (infosource, selectfiles, [('design_id', 'design_id')]),
    (infosource, selectfiles, [('contrast_id', 'contrast_id')]),

    (selectfiles, palm_corr, [('design', 'design')]),
    (selectfiles, palm_corr, [('contrast', 'contrast')]),

    (selectfiles, palm_corr_pearson, [('design', 'design')]),
    (selectfiles, palm_corr_pearson, [('contrast', 'contrast')]),

    (palm_corr, datasink, [('P_values', 'P_values')]),
    (palm_corr_pearson, datasink, [('corr_coefs', 'corr_coefs')]),

])


resting_state_corr.write_graph(graph2use='colored', format='svg', simple_form=True)
resting_state_corr.run(plugin='SLURM', plugin_args={
                       'dont_resubmit_completed_jobs': True, 'max_jobs': 50, 'sbatch_args': '--mem=32G'})
# plugin_args={'sbatch_args': '--time=24:00:00 -N1 -c2 --mem=40G','max_jobs':200}
# resting_state_corr.run('MultiProc', plugin_args={'n_procs': 8})
