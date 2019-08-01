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

# location for AAOutputFile3 and Test18_OF2 files
input_dir = r"C:\\openfast-noise-3\noite-test\_outputs-OF2"

# desired location for processed results
output_dir = r"C:\\Users\mphillip\Documents\openfast\Poster Images-Data\New Model"

# appended name for AAOutputFile3: (i.e. yaw10deg_AAOutputFile3.out => outputname = "yaw10deg_". Leave outputname = "" if no modification
outputname = ""
AAname = outputname + "AAOutputFile3.out"
OF2name = outputname + "Test18_OF2.out"

# save plot and/or data?
save_fig = True
save_data = True

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
n = 1
rpm = OF2[["RotSpeed_[rpm]"]].mean()[0]
time_revs = n*60/rpm
tot_time = AA_3["Time_[s]"].max()
sample_time = tot_time - time_revs

# slice AA dataframe for t > sample_time
AA_3 = AA_3[AA_3["Time_[s]"] > sample_time]
AA_3=AA_3.drop("Time_[s]",axis=1)

# convert observer Sound Pressure Level (SPL) to Sound Pressure (P)
AA_3 = 10**(AA_3/10)

# average P for each observer
AA_3 = AA_3.mean()

# conver back from P to SPL
AA_3 = 10*np.log10(AA_3)

# convert to dataframe with appropriate columns
cols = ['Obs','Mech','Freq','SPL']
aa_3 = pd.DataFrame(columns=cols)
for i in AA_3.index:
    nums = re.findall(r"[-+]?\d*\.\d+|\d+",i)
    aa_3.loc[len(aa_3)] = [nums[0],nums[2],nums[1],AA_3[i]]

AA_3 = aa_3
AA_3=AA_3.apply(pd.to_numeric)

#plot stuff
# TODO loop plot to include all observers with appropriate legend
plt.xscale('log')
plt.ylabel('SPL (dB)')
plt.xlabel('Frequency (Hz)')
line1,=plt.plot(AA_3[(AA_3["Obs"] == 1) & (AA_3["Mech"] == 1)]["Freq"],AA_3[(AA_3["Obs"] == 1) & (AA_3["Mech"] == 1)].where(AA_3["SPL"]>0)["SPL"], label="LBL")
line2,=plt.plot(AA_3[(AA_3["Obs"] == 1) & (AA_3["Mech"] == 2)]["Freq"],AA_3[(AA_3["Obs"] == 1) & (AA_3["Mech"] == 2)].where(AA_3["SPL"]>0)["SPL"], label="TBLP")
line3,=plt.plot(AA_3[(AA_3["Obs"] == 1) & (AA_3["Mech"] == 3)]["Freq"],AA_3[(AA_3["Obs"] == 1) & (AA_3["Mech"] == 3)].where(AA_3["SPL"]>0)["SPL"], label="TBLS")
line4,=plt.plot(AA_3[(AA_3["Obs"] == 1) & (AA_3["Mech"] == 4)]["Freq"],AA_3[(AA_3["Obs"] == 1) & (AA_3["Mech"] == 4)].where(AA_3["SPL"]>0)["SPL"], label="SEP")
line5,=plt.plot(AA_3[(AA_3["Obs"] == 1) & (AA_3["Mech"] == 5)]["Freq"],AA_3[(AA_3["Obs"] == 1) & (AA_3["Mech"] == 5)].where(AA_3["SPL"]>0)["SPL"], label="Blunt")
line6,=plt.plot(AA_3[(AA_3["Obs"] == 1) & (AA_3["Mech"] == 6)]["Freq"],AA_3[(AA_3["Obs"] == 1) & (AA_3["Mech"] == 6)].where(AA_3["SPL"]>0)["SPL"], label="TIP")
line7,=plt.plot(AA_3[(AA_3["Obs"] == 1) & (AA_3["Mech"] == 7)]["Freq"],AA_3[(AA_3["Obs"] == 1) & (AA_3["Mech"] == 7)].where(AA_3["SPL"]>0)["SPL"], label="Inflow")
plt.legend(handles=[line1,line2,line3,line4,line5,line6,line7])
if save_fig == True:
    plt.save('{}-contour.png'.format(outputfilename))

plt.show()

# export to csv
if save_data == True:
    AA_3.to_csv(r'{}-data.csv'.format(outputfilename))




