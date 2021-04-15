# plot the correlation between the amplitude and the behavior
# since only amplitude was correlated with behavioral markaers
# reminder from the matlab script, the behaviorla markers with significant values were:
# TODO: compare the final plots between mac and linux
# EPM_open_to_close_ratio_p_corrected_A
# EPM_time_in_closed_arms_p_corrected_A
# EPM_time_in_closed_arms_percent_p_corrected_A
# EPM_time_in_opened_arms_p_corrected_A
# EPM_time_in_opened_arms_percent_p_corrected_A

import numpy as np
import matplotlib.pyplot as plt
import nipype.interfaces.fsl as fsl
import ntpath
import sys
import matplotlib
import os
