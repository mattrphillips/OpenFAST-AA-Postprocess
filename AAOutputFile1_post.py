#########################################################################################################################################

# Created by Matt Phillips
# National Renewable Energy Laboratory
# Summer 2019

#########################################################################################################################################
#########################################################################################################################################

# Processes OpenFAST Aeroacoustic output file number 1 (AAOutputFile1) which gives overall sound pressure level (OASPL) for each observer

#########################################################################################################################################

#packages

#########################################################################################################################################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from spectral import fft_wrap
import weio
from parse import *
import re
import matplotlib.colors

#########################################################################################################################################

## User inputs

# location for AAOutputFile1, Test18_OF2, and AA_ObserverLocations files
input_dir = r"C:\\Users\mphillip\Documents\openfast\Poster Images-Data"
loc_dir = r"C:\openfast-noise-3\noite-test\5MW_Baseline"

# desired location for processed results
output_dir = "..\\openfast\\Poster Images-Data\\New model"

# appended name for AAOutputFile1: (i.e. yaw10deg_AAOutputFile1.out => outputname = "yaw10deg_". Leave outputname = "" if no modification
outputname = "6mps-"
AAname = outputname + "AAOutputFile1.out"
OF2name = outputname + "Test18_OF2.out"

# location file name
locname = "AA_ObserverLocations_grid.dat"

# save plot and/or data?
save_fig = True
save_data = True

#########################################################################################################################################

# produces full path
AAfilename = input_dir + '\\' + AAname
OF2filename = input_dir + '\\' + OF2name
locfilename = loc_dir + '\\' + locname
outputfilename = output_dir + '\\' + outputname + "AAOutputFile1"

# reads in file data
AA_1 = weio.FASTOutFile(AAfilename).toDataFrame()
OF2 = weio.FASTOutFile(OF2filename).toDataFrame()
location = pd.read_csv(locfilename,delimiter='\s+',skiprows=[0],names=['x','y','z'])

# determine number of observers
num_obs = AA_1.shape[1]-1

# calculate sample time for n revolutions
n = 1
rpm = OF2[["RotSpeed_[rpm]"]].mean()[0]
time_revs = n*60/rpm
tot_time = AA_1["Time_[s]"].max()
sample_time = tot_time - time_revs

# slice AA dataframe for t > sample_time
AA_1 = AA_1[AA_1["Time_[s]"] > sample_time]
AA_1=AA_1.drop("Time_[s]",axis=1)

# convert observer Sound Pressure Level (SPL) to Sound Pressure (P)
AA_1 = 10**(AA_1 / 10)

# average P for each observer
AA_1 = AA_1.mean()

# conver back from P to SPL
AA_1 = 10*np.log10(AA_1)

# merge location info with SPL info
AA_1=AA_1.reset_index()
AA_1=AA_1.drop("index",axis=1)
AA_1=pd.merge(location,AA_1,left_index=True,right_index=True)
AA_1=AA_1.rename(index=str,columns={0:"SPL"})

# contour plot of SPL for each location
x=AA_1['x'];
y=AA_1['y'];
z=AA_1['SPL'];

fig1,ax1=plt.subplots()
ax1.set_aspect('equal')
ax1.set_title('SPL Contour at 2m Height')
ax1.set_xlabel('x [m]')
ax1.set_ylabel('y [m]')
tcf=ax1.tricontourf(x,y,z,)
fig1.colorbar(tcf,orientation="horizontal")
ax1.tricontour(x,y,z,colors='None')
if save_fig = True:
    plt.savefig('{}-contour.png'.format(outputfilename))

plt.show()

# export to csv
if save_data = True:
    AA_1.to_csv(r'{}-data.csv'.format(output_dir))

