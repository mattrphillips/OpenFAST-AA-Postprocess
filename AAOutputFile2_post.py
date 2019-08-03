#########################################################################################################################################

# Created by Matt Phillips
# National Renewable Energy Laboratory
# Summer 2019

#########################################################################################################################################
#########################################################################################################################################

# Processes OpenFAST Aeroacoustic output file number 2 (AAOutputFile2) which gives sound pressure level (SPL) spectra for each observer

# NOTE: currently only supports one observer location

#########################################################################################################################################

#packages

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import weio
from parse import *
import re

#########################################################################################################################################

## User inputs

# location for AAOutputFile2 and Test18_OF2 files
input_dir = r"C:\\openfast-noise-3\noite-test\_outputs-OF2"

# desired location for processed results
output_dir = "..\\openfast\\Poster Images-Data\\New Model"

# appended name for AAOutputFile2: (i.e. yaw10deg_AAOutputFile2.out => outputname = "yaw10deg_". Leave outputname = "" if no modification
outputname = ""
AAname = outputname + "AAOutputFile2.out"
OF2name = outputname + "Test18_OF2.out"

# save plot and/or data?
save_fig = True
save_data = True

#########################################################################################################################################

# produces full path
AAfilename = input_dir + '\\' + AAname
OF2filename = input_dir + '\\' + OF2name
outputfilename = output_dir + '\\' + "AAOutputFile2"

# read in file data
AA_2 = weio.FASTOutFile(AAfilename).toDataFrame()
OF2 = weio.FASTOutFile(OF2filename).toDataFrame()

# determine number of observers
num_obs = AA_2.shape[1]-1

# calculate sample time for n revolutions
n = 1
rpm = OF2[["RotSpeed_[rpm]"]].mean()[0]
time_revs = n*60/rpm
tot_time = AA_2["Time_[s]"].max()
sample_time = tot_time - time_revs

# slice AA dataframe for t > sample_time
AA_2 = AA_2[AA_2["Time_[s]"] > sample_time]
AA_2=AA_2.drop("Time_[s]",axis=1)

# convert observer Sound Pressure Level (SPL) to Sound Pressure (P)
AA_2 = 10**(AA_2/10)

# average P for each observer
AA_2 = AA_2.mean()

# conver back from P to SPL
AA_2 = 10*np.log10(AA_2)

# convert to dataframe with appropriate columns
cols = ['Obs','Freq','SPL']
aa_2 = pd.DataFrame(columns=cols)
for i in AA_2.index:
    nums = re.findall(r"[-+]?\d*\.\d+|\d+",i)
    aa_2.loc[len(aa_2)] = [nums[0],nums[1],AA_2[i]]

AA_2 = aa_2
AA_2=AA_2.apply(pd.to_numeric)

#plot stuff
plt.xscale('log')
plt.ylabel('SPL (dB)')
plt.xlabel('Frequency (Hz)')
line1,=plt.plot(AA_2[AA_2["Obs"] == 1]["Freq"],AA_2[AA_2["Obs"] == 1].where(AA_2["SPL"]>0)["SPL"], label="0 degrees (downwind)")
plt.legend(handles=[line1,line2])
if save_fig == True:
    plt.savefig(r'{}-contour.png'.format(outputname))

plt.show()

# export to csv
if save_data == True:
    AA_2.to_csv(r'{}-data.csv'.format(outputfilename))




