#This workflow to regress out the bad-components from the 5.75-5.75-18.2 high-passed-smoothed files
#Then to transfer them to the study-template by comibing the rigid transfromation from example 2 anatomical 
#image and the non-rigid trasnformations from anato to study based template


#Start by importing respective modules:

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

#------------------------------------------------------------------------------------------------------------
# In[2]:

experiment_dir = '/media/amr/Amr_4TB/Work/October_Acquistion/' 
#total 33
#288 -> hydrocephaly
#271, 272 -> medtomidine and died
subject_list = ['229', '230', '232', '233', '234', 
                '235', '236', '237', '242', '243', 
                '244', '245', '252', '253', '255', 
                '261', '262', '263', '264', '273',
                '274', '281', '282', '286', '287', 
                '362', '363', '364', '365', '366']

# subject_list = ['229']

output_dir  = '/Volumes/Amr_1TB/resting_state/resting_state_metaflow_outputdir'
working_dir = '/Volumes/Amr_1TB/resting_state/resting_state_metaflow_workingdir'

metaflow = Workflow (name = 'metaflow')

metaflow.base_dir = opj(experiment_dir, working_dir)


#------------------------------------------------------------------------------------------------------------
# In[3]:

infosource = Node(IdentityInterface(fields=['subject_id']),
                  name="infosource")
infosource.iterables = [('subject_id', subject_list)]


#Remember, I ran BiasField correction then I eroded the brain, that's what I am using
#also, after comparison, I choose smoothing with 4 kernel, it looks much better than bigger kernels



templates = {                                 
             'Anat'                         : '/Volumes/Amr_1TB/resting_state/resting_state_preproc_outputdir/anat_brain/{subject_id}/Anat_Bet_{subject_id}_corrected_ero.nii.gz',

             'Filtered_Smoothed_rs_fMRI'    : '/Volumes/Amr_1TB/resting_state/resting_state_preproc_outputdir/preproc_img/{subject_id}/fwhm-4.4.0/afni_2d_smoothed_maths_filt_maths.nii.gz',

             'Melodic_Mix'                  : '/Volumes/Amr_1TB/resting_state/resting_state_preproc_outputdir/melodic/{subject_id}/fwhm-4.4.0/_dim_20/melodic.ica/melodic_mix',

             'example2Anat'                 : '/Volumes/Amr_1TB/resting_state/resting_state_preproc_outputdir/func_2_anat_transformations/{subject_id}/transformComposite.h5',

             'Anat2Template'                : '/Volumes/Amr_1TB/resting_state/resting_state_preproc_outputdir/anat_2_temp_transformations/{subject_id}/transformComposite.h5',

             'labels'                       : '/Volumes/Amr_1TB/resting_state/resting_state_preproc_outputdir/melodic/{subject_id}/fwhm-4.4.0/_dim_20/melodic.ica/labels'

             }
selectfiles = Node(SelectFiles(templates,
                    base_directory=experiment_dir),
                   name="selectfiles")

#------------------------------------------------------------------------------------------------------------
# In[4]:

datasink = Node(DataSink(), name = 'datasink')
datasink.inputs.container = output_dir
datasink.inputs.base_directory = experiment_dir


substitutions = [('_subject_id_', '')]

datasink.inputs.substitutions = substitutions


#fsl.FSLCommand.set_default_output_type('NIFTI') #extremly stupid idea, the preproc folder went from 236 GB -> 35 GB

#-----------------------------------------------------------------------------------------------------
# In[5]:

template_brain = '/Volumes/Amr_1TB/anat_temp_new/anat_temp_enhanced_3.nii.gz' # a new template with 8 iterationsand -thr 5 mask then multiply the original template to remove blurry edges 
template_mask = '/Volumes/Amr_1TB/anat_temp_new/anat_template_enhanced_mask_2.nii.gz'

TR = 2.0
 
#-----------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------
# In[6]:

# I Have calssified the melodic ICs outputs of each subject to signal or artefact
# and saved them in an csv file and wrote function to extract them from theis csv file

#this is no longer necessary, since I am using labels files now after classification using MELODIC layout
# Bad_Components_CSV_File = '/media/amr/Amr_4TB/Work/October_Acquistion/Bad_Components_fwhm_4_dim_20.csv'



#-----------------------------------------------------------------------------------------------------
# In[7]:
# In[7]:
#this is the old function
#If you put all the bad components in the same csv file

# def get_bad_components(subject_id, csv_file):
#     import numpy as np
#     bad_components = np.genfromtxt(csv_file, delimiter=',')
 
#     #convert the array into int
#     bad_components = bad_components.astype(int)
#     subject_id = int(subject_id)
#     print (subject_id)
    
#     #get the row corresponding to each subject_id
#     components = bad_components[bad_components[:,0] == subject_id]
    
#     #get rid of the -9223372036854775808 I got after converting to nan
#     components = components[components > 0]
    
#     #convert to list to work as an appropriate input to fsl_regfilt
#     #the index to remove the subject_id
#     components = list(components)[1:]
    
#     #print the bad components
#     print (components)
#     return components

# get_bad_components = Node(name = 'get_bad_components',
#                           interface = Function(input_names = ['subject_id', 'csv_file'],
#                                                output_names = ['components'],
#                                                function = get_bad_components))

# get_bad_components.inputs.csv_file = Bad_Components_CSV_File


#-----------------------------------------------------------------------------------------------------
#this function works when you use the MELODIC layout, classify the components and later use
#the labels file as an input
# N.B, I copied Melodic file in the outdir to Melodic.ica as it opens better with fsleyes

def get_bad_components(labels):
        fh = open(labels)
        lines = fh.readlines()
        components_str = (lines[len(lines)-1])

        components_list =  eval('[' + components_str[0:-1]  + ']')[0] #[0:-1] to remove \n at the end, '[' to remove extra two brackets
        print(components_list)
        
        return components_list
        

get_bad_components = Node(name = 'get_bad_components',
                          interface = Function(input_names = ['labels'],
                                               output_names = ['components_list'],
                                               function = get_bad_components))

#-----------------------------------------------------------------------------------------------------
# In[8]:
#Define the fsl.regfilt Node
regfilt = Node (fsl.FilterRegressor(), name = 'Filter_Regressors')




#-----------------------------------------------------------------------------------------------------
# In[9]:
antsApply = Node(ants.ApplyTransforms(), name = 'antsApply')
antsApply.inputs.dimension = 3

antsApply.inputs.input_image_type = 3
antsApply.inputs.num_threads = 1
antsApply.inputs.float = True

antsApply.inputs.reference_image = template_brain


#-----------------------------------------------------------------------------------------------------
# In[10]:
#Merge the trasnforms
merge_transforms = Node(Merge(2), name = 'merge_transforms')



#-----------------------------------------------------------------------------------------------------
# In[11]:
#write an appended list of the names of the files that enter the melodic
def write_name(in_file):
    f = open('/Volumes/Amr_1TB/resting_state/resting_state_metaflow_workingdir/melodic_list_october_acquistions.txt', 'a')
    print (in_file)
    f.write('\n' + in_file)
    f.close()


write_name = Node(name = 'write_name', 
                interface = Function(input_names = ['in_file'],

                                    function = write_name))





#-----------------------------------------------------------------------------------------------------
# In[12]:
#Connect the nodes:

metaflow.connect ([
                    (infosource, selectfiles,[('subject_id','subject_id')]),
                    (infosource, get_bad_components, [('subject_id','subject_id')]),
                    (selectfiles, regfilt, [('Filtered_Smoothed_rs_fMRI','in_file')]),
                    (selectfiles, regfilt, [('Melodic_Mix','design_file')]),

                    (selectfiles, get_bad_components, [('labels','labels')]),
                    (get_bad_components, regfilt, [('components_list','filter_columns')]),


                    (selectfiles, merge_transforms, [('Anat2Template','in1')]),
                    (selectfiles, merge_transforms, [('example2Anat','in2')]),


                    (regfilt, antsApply, [('out_file','input_image')]),
                    (merge_transforms, antsApply, [('out','transforms')]),

                    (antsApply, write_name, [('output_image','in_file')]),

                    #==================================================================================
                    (antsApply, datasink, [('output_image','func_filt_temp_space')]),



    ])


metaflow.write_graph(graph2use='colored', format='png', simple_form=True)
metaflow.run('MultiProc', plugin_args={'n_procs': 16})

