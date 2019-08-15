#########################################################################################################################################

# Created by Matt Phillips
# National Renewable Energy Laboratory
# Summer 2019

#########################################################################################################################################
#########################################################################################################################################

# Processes OpenFAST Aeroacoustic output file number 2 (AAOutputFile2) which gives sound pressure level (SPL) spectra for each observer

# NOTE: recommended to only use small number of observers for plotting purposes. CSV data can support any number of observers.

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

# location for AAOutputFile3 and Test18_OF2 files
input_dir = r"C:\\openfast-noise-3\noite-test\_outputs-OF2"

# desired location for processed results
output_dir = r"C:\\Users\mphillip\Documents\openfast\Poster Images-Data\New Model"

# appended name for AAOutputFile3: (i.e. yaw10deg_AAOutputFile3.out => outputname = "yaw10deg_". Leave outputname = "" if no modification
outputname = ""
AAname = outputname + "AAOutputFile3.out"
OF2name = outputname + "Test18_OF2.out"

# number of revolutions (n) to calculate SPL
n = 1

# save plot and/or data?
plt_grid = True            # creates subplot for each observer if True
save_fig = False
save_data = False

#########################################################################################################################################

# produces full path
AAfilename = input_dir + '\\' + AAname
OF2filename = input_dir + '\\' + OF2name
outputfilename = output_dir + '\\' + outputname + "AAOutputFile3"

# read file data
AA_3 = weio.FASTOutFile(AAfilename).toDataFrame()
OF2 = weio.FASTOutFile(OF2filename).toDataFrame()

# determine number of observers
num_obs = (AA_3.shape[1]-1)/(7*34)

# calculate sample time for n revolutions
rpm = OF2[["RotSpeed_[rpm]"]].mean()[0]
time_revs = n*60/rpm
tot_time = AA_3["Time_[s]"].max()
if time_revs < tot_time:
    sample_time = tot_time - time_revs
else:
    print("Error: Time for number of revolutions exceeds simulation time. Reduce n.")
    raise SystemExit('')

# slice AA dataframe for t > sample_time
AA_3 = AA_3[AA_3["Time_[s]"] > sample_time]
AA_3=AA_3.drop("Time_[s]",axis=1)

# convert observer Sound Pressure Level (SPL) to Sound Pressure (P)
AA_3 = 10**(AA_3/10)

# average P for each observer
AA_3 = AA_3.mean()

# convert back from P to SPL
if any(AA_3[i] == 0 for i in range(0,AA_3.size)):
    print('Error: Log of zero encountered.')
    raise SystemExit('')
else:
    AA_3 = 10*np.log10(AA_3)

# convert to dataframe with appropriate columns
cols = ['Observer','Mechanism','Frequency (Hz)','SPL (dB)']
aa_3 = pd.DataFrame(columns=cols)
for i in AA_3.index:
    nums = re.findall(r"[-+]?\d*\.\d+|\d+",i)
    aa_3.loc[len(aa_3)] = [nums[0],nums[2],nums[1],AA_3[i]]

AA_3 = aa_3

# rename mechanism for legend
for i in range(0,AA_3.last_valid_index()+1):
    if AA_3.loc[i,"Mechanism"]=='1':
        AA_3.loc[i,"Mechanism"]="LBL"
    if AA_3.loc[i,"Mechanism"]=='2':
        AA_3.loc[i,"Mechanism"]="TBL-Pressure"
    if AA_3.loc[i,"Mechanism"]=='3':
        AA_3.loc[i,"Mechanism"]="TBL-Suction"
    if AA_3.loc[i,"Mechanism"]=='4':
        AA_3.loc[i,"Mechanism"]="Separation"
    if AA_3.loc[i,"Mechanism"]=='5':
        AA_3.loc[i,"Mechanism"]="Blunt"
    if AA_3.loc[i,"Mechanism"]=='6':
        AA_3.loc[i,"Mechanism"]="Tip"
    if AA_3.loc[i,"Mechanism"]=='7':
        AA_3.loc[i,"Mechanism"]="Inflow"

AA_3["Observer"]=AA_3["Observer"].apply(pd.to_numeric)
AA_3["Frequency (Hz)"]=AA_3["Frequency (Hz)"].apply(pd.to_numeric)
AA_3["SPL (dB)"]=AA_3["SPL (dB)"].apply(pd.to_numeric)

if plt_grid == True:
    # create square grid
    num_cols=np.ceil(np.sqrt(num_obs))

    g=sb.relplot(x="Frequency (Hz)",y="SPL (dB)",hue="Mechanism",col="Observer",col_wrap=num_cols,kind="line",data=AA_3)
    g.set(xscale='log')
    g.set(ylim=(0,None))
else:
    # plot if number of observers is less than 7. (Only 6 line styles.)
    if num_obs < 7:
        #plot stuff
        plt.xscale('log')
        if num_obs == 1:
            ax=sb.lineplot(x=AA_3["Frequency (Hz)"],y=AA_3["SPL (dB)"],hue=AA_3["Mechanism"],legend = "full")
        else:
            ax=sb.lineplot(x=AA_3["Frequency (Hz)"],y=AA_3["SPL (dB)"],style=AA_3["Observer"],hue=AA_3["Mechanism"],legend = "full")
        ax.legend(loc='center right',bbox_to_anchor=(1.45,0.5))
        plt.subplots_adjust(right=.7)
        ax.set_ylim(0,)

        if save_fig == True:
            plt.save('{}-contour.png'.format(outputfilename))

    else:
        print("Too many observers to generate plot. Maximum number of observers is 6.")

plt.show()

# export to csv
if save_data == True:
    AA_3.to_csv(r'{}-data.csv'.format(outputfilename))




