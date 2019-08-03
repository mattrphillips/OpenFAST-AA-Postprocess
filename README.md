# OpenFAST-AA-Postprocess
Python post processing tools for NREL OpenFAST Aeroacoustic output files

######################################################################################################

AAOutputFile1_post.py
	Description:
	Creates contour plot from Overall Sound Pressure Level (OASPL) at each observer location.
	
	Inputs:
	* Location of AAOutputFile1.out and Test18_OF2.out files
	* Modifiers of both names
	* Location of AA_ObserverLocations.dat files
	* Full name of Obs Loc files
	* Desired directory for processed results
	* Flag for saving csv data and contour plot
	
	Outputs:
	* CSV file for x, y, and OASPL (assuming constant z) of each observer
	* Contour plot of OASPL (requires at least 3 observers)
		
	Known Problems:
	* Many...

######################################################################################################
	
AAOutputFile2_post.py
	Description:
	Creates line plot from Sound Pressure Level (SPL) for each frequency for each observer.
	
	Inputs:
	* Location of AAOutputFile2.out and Test18_OF2.out files
	* Modifiers of both names
	* Desired directory for processed results
	* Flag for saving csv data and contour plot
	
	Outputs:
	* CSV file for Observer, Frequency, and SPL
	* Line plot of frequency-dependent SPL
		
	Known Problems:
	* Currently only supports one observer location
	* Many more...

######################################################################################################
	
AAOutputFile3_post.py
	Description:
	Creates line plot from mechanism-dependent Sound Pressure Level (SPL) for each frequency for each
	observer.
	
	Inputs:
	* Location of AAOutputFile3.out and Test18_OF2.out files
	* Modifiers of both names
	* Desired directory for processed results
	* Flag for saving csv data and contour plot
	
	Outputs:
	* CSV file for Observer, Mechanism, Frequency, and SPL
	* Line plot of mechanism-dependent and frequency-dependent SPL
		
	Known Problems:
	* Currently only supports one observer location
	* Many more...



