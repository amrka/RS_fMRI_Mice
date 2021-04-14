% Set up FSL environment
setenv( 'FSLDIR', '/usr/share/fsl/5.0');
fsldir = getenv('FSLDIR');
fsldirmpath = sprintf('%s/etc/matlab',fsldir);
path(path, fsldirmpath);
%clear fsldir fsldirmpath;


addpath /media/amr/HDD/Softwares/FSLNETS/FSLNets              % wherever you've put this package
addpath /media/amr/HDD/Softwares/FSLNETS/L1precision            % L1precision toolbox
addpath /media/amr/HDD/Softwares/FSLNETS/pwling                 % pairwise causality toolbox
addpath(sprintf('%s/etc/matlab',getenv('FSLDIR')))
%%
n_dims = 20
group_maps='/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_gp_ICA+DR_workingdir/melodic_workflow/_dim_20/melodic_group/melodic_IC';     % spatial maps 4D NIFTI file, e.g. from group-ICA No extension needed
   %%% you must have already run the following (outside MATLAB), to create summary pictures of the maps in the NIFTI file:
   %%% slices_summary <group_maps> 4 $FSLDIR/data/standard/MNI152_T1_2mm <group_maps>.sum
ts_dir='/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_gp_ICA+DR_workingdir/melodic_workflow/_dim_20/dual_regression/output';                           % dual regression output directory, containing all subjects' timeseries

%system('dir=/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_gp_ICA+DR_workingdir/melodic_workflow/_dim_20/melodic_group/;slices_summary ${dir}melodic_IC 3 /media/amr/Amr_4TB/Work/October_Acquistion/anat_temp_enhanced_3.nii.gz ${dir}melodic_IC.sum -1')
%%% [tail: illegal offset -- +] error can be avoided by adding -1 to summary_slices command
%%% it will return one slice image per component instead of three, but here will be no errors
%%% adding -d flag does not pan out very well, the template becomes way too much darker

%%% load timeseries data from the dual regression output directory
ts=nets_load(ts_dir,2,1);
   %%% arg2 is the TR (in seconds)
   %%% arg3 controls variance normalisation: 0=none, 1=normalise whole subject stddev, 2=normalise each separate timeseries from each subject


%%
%%% cleanup and remove bad nodes' timeseries (whichever is NOT listed in ts.DD is *BAD*).
ts.DD=[1,2,4,5,6,7,9,10,11,12,13,14,16,17,18,19,20];  % list the good nodes in your group-ICA output (counting starts at 1, not 0)
% ts.UNK=[10];  optionally setup a list of unknown components (where you're unsure of good vs bad)
ts=nets_tsclean(ts,1);                   % regress the bad nodes out of the good, and then remove the bad nodes' timeseries (1=aggressive, 0=unaggressive (just delete bad)).
                                         % For partial-correlation netmats, if you are going to do nets_tsclean, then it *probably* makes sense to:
                                         %    a) do the cleanup aggressively,
                                         %    b) denote any "unknown" nodes as bad nodes - i.e. list them in ts.DD and not in ts.UNK
                                         %    (for discussion on this, see Griffanti NeuroImage 2014.)
nets_nodepics(ts,group_maps);            % quick views of the good and bad components


% all the netmats are r-to-z transformed
netmats_A= nets_netmats(ts,0,'amp');        % amplitudes only - no correlations (just the diagonal)
netmats_F=  nets_netmats(ts,1,'corr');       % full correlation (normalised covariances)
netmats_P=  nets_netmats(ts,1,'icov');       % partial correlation
netmats_rP=  nets_netmats(ts,1,'ridgep', 0.1);     % Ridge Regression partial, with rho=0.1

[Znet_A,Mnet_A]=nets_groupmean(netmats_A,1);   % test whichever netmat you're interested in; returns Z values from one-group t-test and group-mean netmat
[Znet_F,Mnet_F]=nets_groupmean(netmats_F,1);   % test whichever netmat you're interested in; returns Z values from one-group t-test and group-mean netmat
[Znet_P,Mnet_P]=nets_groupmean(netmats_P,1);   % test whichever netmat you're interested in; returns Z values from one-group t-test and group-mean netmat
[Znet_rP,Mnet_rP]=nets_groupmean(netmats_rP,1);   % test whichever netmat you're interested in; returns Z values from one-group t-test and group-mean netmat


%%
con = {
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_open_to_close_ratio.con';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_time_in_center.con';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_time_in_center_percent.con';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_time_in_closed_arms.con';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_time_in_closed_arms_percent.con';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_time_in_opened_arms.con';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_time_in_opened_arms_percent.con';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_total_distance.con';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_velocity.con';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/OF_percent_in_center.con';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/OF_percent_in_corners.con';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/OF_sec_in_center.con';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/OF_total_distance.con';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/OF_total_time_in_corners.con';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/OF_velocity.con'
};

mat = {
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_open_to_close_ratio.mat';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_time_in_center.mat';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_time_in_center_percent.mat';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_time_in_closed_arms.mat';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_time_in_closed_arms_percent.mat';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_time_in_opened_arms.mat';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_time_in_opened_arms_percent.mat';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_total_distance.mat';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/EPM_velocity.mat';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/OF_percent_in_center.mat';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/OF_percent_in_corners.mat';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/OF_sec_in_center.mat';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/OF_total_distance.mat';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/OF_total_time_in_corners.mat';
'/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/OF_velocity.mat'
};

%%
% do not forget to bring the index of bigger than 0.95
% I created manually a directory :
% /media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/FC_behavior_correlation
% to save the results
i = 1
while i <= length(con)
    design = mat{i};
    contrast = con{i};
    suffix = regexprep(mat{i}, '/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/resting_state_corr_designs/|.mat','');

    [p_uncorrected_A,p_corrected_A]=nets_glm(netmats_A, design, contrast,0);
    save(['/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/FC_behavior_correlation/' suffix '_p_corrected_A.mat'], 'p_corrected_A')

    [p_uncorrected_F,p_corrected_F]=nets_glm(netmats_F, design, contrast,0);
    nets_edgepics(ts,group_maps,Znet_F,reshape(p_corrected_F(1,:),ts.Nnodes,ts.Nnodes),6);
    nets_edgepics(ts,group_maps,Znet_F,reshape(p_corrected_F(2,:),ts.Nnodes,ts.Nnodes),6);
    save(['/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/FC_behavior_correlation/' suffix '_p_corrected_F.mat'], 'p_corrected_F')

    [p_uncorrected_P,p_corrected_P]=nets_glm(netmats_P, design, contrast,0);
    nets_edgepics(ts,group_maps,Znet_P,reshape(p_corrected_P(1,:),ts.Nnodes,ts.Nnodes),6);
    nets_edgepics(ts,group_maps,Znet_P,reshape(p_corrected_P(2,:),ts.Nnodes,ts.Nnodes),6);
    save(['/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/FC_behavior_correlation/' suffix '_p_corrected_P.mat'], 'p_corrected_P')

    [p_uncorrected_rP,p_corrected_rP]=nets_glm(netmats_rP, design, contrast,0);
    nets_edgepics(ts,group_maps,Znet_rP,reshape(p_corrected_rP(1,:),ts.Nnodes,ts.Nnodes),6);
    nets_edgepics(ts,group_maps,Znet_rP,reshape(p_corrected_rP(2,:),ts.Nnodes,ts.Nnodes),6);
    save(['/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/FC_behavior_correlation/' suffix '_p_corrected_rP.mat'], 'p_corrected_rP')
    i = i + 1
end



%%
% N.B. I checked the elements of those structures against the single mats and they checked out
% construct structures containing each filename and its respective pc_corrected_mat
% first the amplitude
corr_mats = dir('/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/FC_behavior_correlation/*_A.mat')

% construct two empty cells, one to hold the filenames and the other the mats
% since when you load the filename, they all have the same name (p_corrected_A)
names = cell(size(corr_mats))
values = cell(size(corr_mats))

% loop over the filenames
for kk = 1:numel(corr_mats)
    names{kk} = corr_mats(kk).name(1:end-4)
    mat_name = load(corr_mats(kk).name)
    values{kk} = mat_name.p_corrected_A
end

% combine the names and their respective mats
p_corrected_A_struc = cell2struct(values, names)
save('/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/FC_behavior_correlation/p_corrected_A_struc')

%%
% the rest
corr_mats = dir('/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/FC_behavior_correlation/*_F.mat')
names = cell(size(corr_mats))
values = cell(size(corr_mats))

for kk = 1:numel(corr_mats)
    names{kk} = corr_mats(kk).name(1:end-4)
    mat_name = load(corr_mats(kk).name)
    values{kk} = mat_name.p_corrected_F
end

p_corrected_F_struc = cell2struct(values, names)
save('/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/FC_behavior_correlation/p_corrected_F_struc')

%%
corr_mats = dir('/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/FC_behavior_correlation/*_P.mat')
names = cell(size(corr_mats))
values = cell(size(corr_mats))

for kk = 1:numel(corr_mats)
    names{kk} = corr_mats(kk).name(1:end-4)
    mat_name = load(corr_mats(kk).name)
    values{kk} = mat_name.p_corrected_P
end

p_corrected_P_struc = cell2struct(values, names)
save('/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/FC_behavior_correlation/p_corrected_P_struc')

%%
corr_mats = dir('/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/FC_behavior_correlation/*_rP.mat')
names = cell(size(corr_mats))
values = cell(size(corr_mats))

for kk = 1:numel(corr_mats)
    names{kk} = corr_mats(kk).name(1:end-4)
    mat_name = load(corr_mats(kk).name)
    values{kk} = mat_name.p_corrected_rP
end

p_corrected_rP_struc = cell2struct(values, names)
save('/media/amr/Amr_4TB/Work/October_Acquistion/resting_state/resting_state_corr/FC_behavior_correlation/p_corrected_rP_struc')
