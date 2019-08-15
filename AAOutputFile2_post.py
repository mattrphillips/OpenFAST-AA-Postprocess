#########################################################################################################################################

# Created by Matt Phillips
# National Renewable Energy Laboratory
# Summer 2019

#########################################################################################################################################
#########################################################################################################################################

# Processes OpenFAST Aeroacoustic output file number 2 (AAOutputFile2) which gives sound pressure level (SPL) spectra for each observer

## TODO: Specify observer location in legend

#########################################################################################################################################

#packages

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import weio
from parse import *
import re
import seaborn as sb

#########################################################################################################################################

## User inputs

# location for AAOutputFile2 and Test18_OF2 files
input_dir = r"C:\\openfast-noise-3\noite-test\_outputs-OF2"

# desired location for processed results
output_dir = "..\\openfast"

# appended name for AAOutputFile2: (i.e. yaw10deg_AAOutputFile2.out => outputname = "yaw10deg_". Leave outputname = "" if no modification
outputname = ""
AAname = outputname + "AAOutputFile2.out"
OF2name = outputname + "Test18_OF2.out"

# number of revolutions (n) to calculate OASPL
n = 1

# save plot and/or data?
save_fig = True
save_data = False

#########################################################################################################################################

# produces full path
AAfilename = input_dir + '\\' + AAname
OF2filename = input_dir + '\\' + OF2name
outputfilename = output_dir + '\\' + "AAOutputFile2"

# read in file data
AA_2 = weio.FASTOutFile(AAfilename).toDataFrame()
OF2 = weio.FASTOutFile(OF2filename).toDataFrame()

# determine number of observers
num_obs = (AA_2.shape[1]-1)/34

# calculate sample time for n revolutions
rpm = OF2[["RotSpeed_[rpm]"]].mean()[0]
time_revs = n*60/rpm
tot_time = AA_2["Time_[s]"].max()
if time_revs < tot_time:
    sample_time = tot_time - time_revs
else:
    print("Error: Time for number of revolutions exceeds simulation time. Reduce n.")
    raise SystemExit('')

# slice AA dataframe for t > sample_time
AA_2 = AA_2[AA_2["Time_[s]"] > sample_time]
AA_2=AA_2.drop("Time_[s]",axis=1)

# convert observer Sound Pressure Level (SPL) to Sound Pressure (P)
AA_2 = 10**(AA_2/10)

# average P for each observer
AA_2 = AA_2.mean()

# convert back from P to SPL
if any(AA_2[i] == 0 for i in range(0,AA_2.size)):
    print('Error: Log of zero encountered.')
    raise SystemExit('')
else:
    AA_2 = 10*np.log10(AA_2)

# convert to dataframe with appropriate columns
cols = ['Observer','Frequency (Hz)','SPL (dB)']
aa_2 = pd.DataFrame(columns=cols)
for i in AA_2.index:
    nums = re.findall(r"[-+]?\d*\.\d+|\d+",i)
    aa_2.loc[len(aa_2)] = [nums[0],nums[1],AA_2[i]]

AA_2 = aa_2
AA_2["Frequency (Hz)"]=AA_2["Frequency (Hz)"].apply(pd.to_numeric)
AA_2["SPL (dB)"]=AA_2["SPL (dB)"].apply(pd.to_numeric)

if num_obs < 7:
    #plot stuff
    plt.xscale('log')
    ax=sb.lineplot(x=AA_2["Frequency (Hz)"],y=AA_2["SPL (dB)"],style=AA_2["Observer"],legend = "full")
    ax.legend(loc='center right',bbox_to_anchor=(1.35,0.5))
    plt.subplots_adjust(right=.75)
    ax.set_ylim(0,)
    
    if save_fig == True:
        plt.savefig(r'{}-contour.png'.format(outputfilename))

    plt.show()
else:
    print("Too many observers to generate plot. Maximum number of observers is 6.")

# export to csv
if save_data == True:
    AA_2.to_csv(r'{}-data.csv'.format(outputfilename))




