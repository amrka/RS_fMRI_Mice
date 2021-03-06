# In[1]:

from nipype import config
cfg = dict(execution={'remove_unnecessary_outputs': False})
config.update_config(cfg)

import nipype.interfaces.fsl as fsl
import nipype.interfaces.afni as afni
import nipype.interfaces.ants as ants
import nipype.interfaces.spm as spm

from nipype.interfaces.utility import IdentityInterface, Function, Select, Merge
from os.path import join as opj
from nipype.interfaces.io import SelectFiles, DataSink
from nipype.pipeline.engine import Workflow, Node, MapNode

import numpy as np
import os, re
import matplotlib.pyplot as plt
from nipype.interfaces.matlab import MatlabCommand
MatlabCommand.set_default_paths('/Users/amr/Downloads/spm12')
MatlabCommand.set_default_matlab_cmd("matlab -nodesktop -nosplash")

# import nipype.interfaces.matlab as mlab
# mlab.MatlabCommand.set_default_matlab_cmd("matlab -nodesktop -nosplash")
# mlab.MatlabCommand.set_default_paths('/home/amr/Documents/MATLAB/toolbox/spm8')

#========================================================================================================
# In[2]:

experiment_dir = '/media/amr/Amr_4TB/Work/October_Acquistion/' 
#288 -> hydrocephaly
#271, 272 -> medtomidine and died


subject_list = ['229', '230', '232', '233', '234', 
                '235', '236', '237', '242', '243', 
                '244', '245', '252', '253', '255', 
                '261', '262', '263', '264', '273',
                '274', '281', '282', '286', '287', 
                '362', '363', '364', '365', '366', 
                'Agarose']


# subject_list = ['363']


output_dir  = '/Volumes/Amr_1TB/resting_state/resting_state_preproc_outputdir'
working_dir = '/Volumes/Amr_1TB/resting_state/resting_state_preproc_workingdir'

resting_fmri_preproc = Workflow (name = 'resting_fmri_preproc')
resting_fmri_preproc.base_dir = opj(experiment_dir, working_dir)

#=====================================================================================================
# In[3]:
# Infosource - a function free node to iterate over the list of subject names
infosource = Node(IdentityInterface(fields=['subject_id']),
                  name="infosource")
infosource.iterables = [('subject_id', subject_list)]

#-----------------------------------------------------------------------------------------------------
# In[4]:

templates = {
             'Anat'     : 'Data/{subject_id}/Anat_Bet_{subject_id}.nii',
             'Func'     : 'Data/{subject_id}/rs_fMRI_{subject_id}.nii',
             'Anat_Mask': 'Data/{subject_id}/Mask_{subject_id}.nii',
             }

selectfiles = Node(SelectFiles(templates,
                               base_directory=experiment_dir),
                   name="selectfiles")

#========================================================================================================
# In[5]:

datasink = Node(DataSink(), name = 'datasink')
datasink.inputs.container = output_dir
datasink.inputs.base_directory = experiment_dir

substitutions = [('_subject_id_', ''),('_blurfwhm_bx_by_bz_', 'fwhm-')]
#substitutions = [('_subject_id_', '')]
datasink.inputs.substitutions = substitutions


# fsl.FSLCommand.set_default_output_type('NIFTI') #very stupid idea, it will inflate the size of the folder 


#========================================================================================================
# In[6]:

template_brain = '/Volumes/Amr_1TB/anat_temp_new/anat_temp_enhanced_3.nii.gz' # a new template with 8 iterationsand -thr 5 mask then multiply the original template to remove blurry edges 
template_mask = '/Volumes/Amr_1TB/anat_temp_new/anat_template_enhanced_mask_2.nii.gz'
#I replaced the template that was made from rois of different subject b a template created out of 50 vols of subject 230
epi_brain = '/Volumes/Amr_1TB/resting_state/epi_template/230_template_brain_enhanced.nii.gz'

TR = 2.0

#=======================================================================================================
# In[7]:
#erode the anatomical image to remove the outline that remained after ITK-snap
erode_anat = Node(fsl.ErodeImage(), name='erode_anatomical_image')
erode_anat.inputs.kernel_shape = 'sphere' #this does a better erosion 
erode_anat.inputs.kernel_size = 2.5

#=======================================================================================================
# In[8]:

biasfield_correction_anat = Node(ants.N4BiasFieldCorrection(), name='biasfield_correction_anat')
biasfield_correction_anat.inputs.dimension = 3 
biasfield_correction_anat.inputs.save_bias = True
# biasfield_correction_anat.inputs.output_image = 'anat_bet_biasfield_corrected.nii.gz' #better not to, 
#it confuses the Registration



#======================================================================================================
# In[9]:
#Extract one fmri image to use fro brain extraction, the same one you will use for mcflirt as reference
roi = Node(fsl.ExtractROI(), name='extract_one_fMRI_volume')

roi.inputs.t_min = 375
roi.inputs.t_size = 1

#========================================================================================================
# In[13]:

## normalizing the anatomical_bias_corrected image to the common anatomical template
## Here only we are calculating the paramters, we apply them later.

reg_T1_2_temp = Node(ants.Registration(), name = 'reg_T1_2_temp')
reg_T1_2_temp.inputs.args='--float'
reg_T1_2_temp.inputs.collapse_output_transforms=True
reg_T1_2_temp.inputs.fixed_image=template_brain
reg_T1_2_temp.inputs.initial_moving_transform_com=True
reg_T1_2_temp.inputs.num_threads=4  
reg_T1_2_temp.inputs.output_inverse_warped_image=True
reg_T1_2_temp.inputs.output_warped_image=True
reg_T1_2_temp.inputs.sigma_units=['vox']*3
reg_T1_2_temp.inputs.transforms= ['Rigid', 'Affine', 'SyN']
reg_T1_2_temp.inputs.winsorize_lower_quantile=0.005
reg_T1_2_temp.inputs.winsorize_upper_quantile=0.995
reg_T1_2_temp.inputs.convergence_threshold=[1e-08, 1e-08,1e-08]
reg_T1_2_temp.inputs.convergence_window_size=[10, 10, 10]
reg_T1_2_temp.inputs.metric=['MI', 'MI', 'CC']
reg_T1_2_temp.inputs.metric_weight=[1.0]*3
reg_T1_2_temp.inputs.number_of_iterations=[[1000, 500, 250, 100],
                                           [1000, 500, 250, 100],
                                           [100, 70, 50, 20]]
reg_T1_2_temp.inputs.radius_or_number_of_bins=[32, 32, 4]
reg_T1_2_temp.inputs.sampling_percentage=[0.25, 0.25, 1]
reg_T1_2_temp.inputs.sampling_strategy=['Regular',
                                        'Regular',
                                        'None']
reg_T1_2_temp.inputs.shrink_factors=[[8, 4, 2, 1]]*3
reg_T1_2_temp.inputs.smoothing_sigmas=[[3, 2, 1, 0]]*3
reg_T1_2_temp.inputs.transform_parameters=[(0.1,),
                                           (0.1,),
                                           (0.1, 3.0, 0.0)]
reg_T1_2_temp.inputs.use_histogram_matching=True
reg_T1_2_temp.inputs.write_composite_transform=True
reg_T1_2_temp.inputs.verbose=True
reg_T1_2_temp.inputs.output_warped_image=True
reg_T1_2_temp.inputs.float=True

#========================================================================================================
# In[14]:
coreg = reg_T1_2_temp.clone(name='coregistration')
coreg.inputs.transforms = ['Rigid']
coreg.inputs.metric=['GC']
#========================================================================================================
# In[15]:
# mcflirt -in ${folder} -out ${folder}_mcf  -refvol example_func -plots -mats  -report;

McFlirt = Node(fsl.MCFLIRT(), name = 'McFlirt')
McFlirt.inputs.save_plots = True
McFlirt.inputs.save_mats = True
McFlirt.inputs.save_rms = True


#========================================================================================================
# In[16]:

#Getting motion parameters from Mcflirt and plotting them

def Plot_Motion(motion_par, rms_files):

    import numpy as np
    import matplotlib
    import matplotlib.pyplot as plt
    matplotlib.use('Agg') 

    movement = np.loadtxt(motion_par)
    abs_disp = np.loadtxt(rms_files[0])
    rel_disp = np.loadtxt(rms_files[1])
    plt.figure(figsize=(8,10), dpi=300)

    plt.subplot(311)
    plt.title('Translations in mm')
    plt.plot(movement[:,:3])
    plt.legend(['x','y','z'])

    plt.subplot(312)
    plt.title('Rotations in radians')
    plt.plot(movement[:,3:])
    plt.legend(['x','y','z'])
    
    plt.subplot(313)
    plt.title('Displacement in mm')
    plt.plot(abs_disp)
    plt.plot(rel_disp)
    plt.legend(['abs', 'rel'])

    plt.savefig('Motion')


Plot_Motion = Node(name = 'Plot_Motion',
                  interface = Function(input_names = ['motion_par','rms_files'],
                  function = Plot_Motion))

#=======================================================================================================
# In[10]:
#remove the skull from the epi images
#this is a little bit tricky:
# 1-resample eroded_anat to roi
# 2-apply coreg inverse transformations to get the anat to the space of func
# 3-mask the anat_2_func that is now resmapled to epi
# 4-use this mask to bet the epi

#I also created an epi_mask, removed the skull manually
#I then tried antsRegistration(Not antsBrainExtraction) the results were pretty good
#compared to this method, the registration to epi_template is much more satisfactory


#the epi_template method is as follow:
#1- register the roi volume to epi_mask that is skull stripped
#2- binarize the InverseWarped image using -thr 2
#3- uses this mask to extract brain

# def create_roi_mask(roi, anat, anat_2_func_trans):
#         from nilearn import image
#         import nipype.interfaces.fsl as fsl
#         import nipype.interfaces.ants as ants
#         import os

#         resampled_anat = image.resample_to_img(source_img=anat, target_img=roi)
#         resampled_anat.to_filename('resampled_anat.nii.gz')
#         new_anat = os.path.abspath('resampled_anat.nii.gz')


#         anat_2_func = ants.ApplyTransforms()
#         anat_2_func.inputs.dimension = 3
#         anat_2_func.inputs.input_image = new_anat
#         anat_2_func.inputs.reference_image = roi
#         anat_2_func.inputs.transforms = anat_2_func_trans

#         anat_2_func.inputs.input_image_type = 3
#         anat_2_func.inputs.num_threads = 1
#         anat_2_func.inputs.float = True
#         print(anat_2_func.cmdline)

#         output = anat_2_func.run()
#         out_anat_2_func = output.outputs.output_image




#         mask_resampled = fsl.ImageMaths()
#         mask_resampled.inputs.op_string = '-thr 1 -bin'
#         mask_resampled.inputs.in_file = out_anat_2_func
#         output = mask_resampled.run()
#         bold_mask = output.outputs.out_file
#         # bold_mask.to_filename('bold_mask.nii.gz'
#         # bold_mask = os.path.abspath('bold_mask.nii.gz')


#         return bold_mask

# create_roi_mask = Node(Function(input_names = ['roi', 'anat', 'anat_2_func_trans'],
#                         output_names = ['bold_mask'],
#                         function = create_roi_mask),
#                         name = 'create_roi_mask')

roi_2_epi_temp = reg_T1_2_temp.clone(name='roi_2_epi_temp')
roi_2_epi_temp.inputs.moving_image=epi_brain
roi_2_epi_temp.inputs.convergence_threshold=[1e-012]
roi_2_epi_temp.inputs.transforms= ['Rigid']
roi_2_epi_temp.inputs.metric=['GC']

create_roi_mask = Node(fsl.ImageMaths(), 'create_roi_mask')
create_roi_mask.inputs.op_string = '-bin'


#=======================================================================================================
# In[11]:

brain_extraction_roi = Node(fsl.ApplyMask(), name='brain_extraction_roi')
#======================================================================================================
# In[12]:

brain_extraction_bold = Node(fsl.ApplyMask(), name='brain_extraction_bold')

#========================================================================================================
# In[17]:

# apply the trasnfromation to all the EPI volumes

func_2_template = Node(ants.ApplyTransforms(), name = 'func_2_template')
func_2_template.inputs.dimension = 3

func_2_template.inputs.input_image_type = 3
func_2_template.inputs.num_threads = 1
func_2_template.inputs.float = True


#========================================================================================================
# In[18]:
#obsolete
smoothing = Node(fsl.Smooth(), name = 'smoothing')
smoothing.iterables = ('fwhm', [4, 5, 5.75, 6.25])


#========================================================================================================
#2D smoothing
smoothing_2d = Node(afni.Merge(), name = 'smoothing_2d')
smoothing_2d.inputs.out_file = 'afni_2d_smoothed.nii.gz'
smoothing_2d.inputs.doall = True
smoothing_2d.iterables = ('blurfwhm_bx_by_bz', [[0,0,0], [3,3,0],[4,4,0],[5,5,0]])


#========================================================================================================
# In[18]:

#Getting median intensity
Median_Intensity = Node(fsl.ImageStats(), name = 'Median_Intensity')
#Put -k before -p 50
Median_Intensity.inputs.op_string = '-k %s -p 50'

#Scale median intensity 
def Scale_Median_Intensity (median_intensity):
    scaling = 10000/median_intensity
    return scaling

Scale_Median_Intensity = Node(name = 'Scale_Median_Intensity',
                      interface = Function(input_names = ['median_intensity'],
                                           output_names = ['scaling'],
                                           function = Scale_Median_Intensity))
#========================================================================================================
# In[20]:

#Global Intensity Normalization by multiplying by the scaling value
#the grand-mean intensity normalisation factor ( to give a median brain intensity of 10000 )
#grand mean scaling
Intensity_Normalization = Node(fsl.BinaryMaths(), name = 'Intensity_Normalization')
Intensity_Normalization.inputs.operation = 'mul'

#========================================================================================================
# In[21]:

#   fslmaths ${folder}_mcf_2highres_intnorm -bptf 25 -1 -add tempMean ${folder}_mcf_2highres_tempfilt;
# sigma[vol] = filter_width[secs]/(2*TR[secs])
high_pass_filter = Node(fsl.TemporalFilter(), name = 'high_pass_filter')
high_pass_filter.inputs.highpass_sigma = 25 #100s / (2*2(TR))
#========================================================================================================
# In[22]

#Get the mean image
Get_Mean_Image = Node(fsl.MeanImage(), name = 'Get_Mean_Image')
Get_Mean_Image.inputs.dimension = 'T'

#Add the mean image to the filtered image
Add_Mean_Image = Node(fsl.BinaryMaths(), name = 'Add_Mean_Image')
Add_Mean_Image.inputs.operation = 'add'



#========================================================================================================
# In[23]:

melodic = Node(fsl.MELODIC(), name = 'Melodic')
melodic.inputs.out_dir =  'melodic.ica'
melodic.inputs.approach = 'concat'
melodic.inputs.no_bet = True
melodic.inputs.bg_threshold = 10.0
melodic.inputs.tr_sec = 2.00
melodic.inputs.mm_thresh = 0.5
melodic.inputs.out_all = True
melodic.inputs.report = True
melodic.iterables = ('dim', [15,20,25])


#========================================================================================================
# In[24]:


resting_fmri_preproc.connect([


              (infosource, selectfiles,[('subject_id','subject_id')]),
              (selectfiles, biasfield_correction_anat, [('Anat','input_image')]),

              (biasfield_correction_anat, erode_anat,[('output_image','in_file')]),


              (erode_anat, reg_T1_2_temp, [('out_file','moving_image')]),


              (selectfiles, roi, [('Func','in_file')]),


              (selectfiles, McFlirt, [('Func','in_file')]),
              (roi, McFlirt, [('roi_file','ref_file')]),

              (McFlirt, Plot_Motion, [('par_file','motion_par'),
                                      ('rms_files','rms_files')]),

              (roi, coreg, [('roi_file','moving_image')]),
              (erode_anat, coreg, [('out_file','fixed_image')]),


              (roi, roi_2_epi_temp, [('roi_file','fixed_image')]),

              (roi_2_epi_temp, create_roi_mask, [('warped_image','in_file')]),



              (roi, brain_extraction_roi, [('roi_file','in_file')]),
              (create_roi_mask, brain_extraction_roi, [('out_file','mask_file')]),



              (create_roi_mask, brain_extraction_bold, [('out_file','mask_file')]),
              (McFlirt, brain_extraction_bold, [('out_file','in_file')]),





              (brain_extraction_bold, smoothing_2d, [('out_file','in_files')]),


              (brain_extraction_bold, Median_Intensity, [('out_file','in_file')]),
              (create_roi_mask, Median_Intensity, [('out_file','mask_file')]),

              (Median_Intensity, Scale_Median_Intensity, [('out_stat','median_intensity')]),

              (Scale_Median_Intensity, Intensity_Normalization, [('scaling','operand_value')]),
              (smoothing_2d, Intensity_Normalization, [('out_file','in_file')]),


              (Intensity_Normalization, Get_Mean_Image, [('out_file','in_file')]),
              (Intensity_Normalization, high_pass_filter, [('out_file','in_file')]),

              (high_pass_filter, Add_Mean_Image, [('out_file','in_file')]),
              (Get_Mean_Image, Add_Mean_Image, [('out_file','operand_file')]),

              (Add_Mean_Image, melodic, [('out_file','in_files')]),

              # ======================================datasink============================================
              (Add_Mean_Image, datasink, [('out_file','preproc_img')]),
              (coreg, datasink, [('composite_transform','func_2_anat_transformations')]), #does not work for this particular node

              (brain_extraction_roi, datasink, [('out_file','bold_brain')]),
              

              (erode_anat, datasink, [('out_file','anat_brain')]),
              (reg_T1_2_temp, datasink, [('composite_transform','anat_2_temp_transformations'),
                                              ('warped_image','anat_2_temp_image')]),

              (melodic, datasink, [('out_dir','melodic')])

              ])

resting_fmri_preproc.write_graph(graph2use='colored', format='png', simple_form=True)

# resting_fmri_preproc.run(plugin='SLURM',plugin_args={'dont_resubmit_completed_jobs': True, 'max_jobs':50})
resting_fmri_preproc.run('MultiProc', plugin_args={'n_procs': 16})
