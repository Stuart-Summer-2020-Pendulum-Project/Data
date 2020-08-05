# Last Edited by Rebecca Nishdide 07/13/2020

"""
This file holds data extraction code
Data files frome experiments and the corresponding logs need to be in the working directory, with the titles and format that they are automatically assigned

It is important to follow correct directory structure to maintain organization and accuracy

The file will take user input in the form the experiment number to know which files to extract from

This library should be imported at the beggining of each analysis script for use

"""

import numpy as np
import file_readlines as fr


"""
retrieve user input
"""

exp = input("\nInput the number corresponding to the internal measurement experiment you wish to analyze: ")

"""
use input to find data file from TOF I2C data acqusition. Data file should be in working directory.
"""

DOF_fn = '9DOF_Dat'+ str(exp) + '.txt'
DOF_data = list(fr.file_readlines(DOF_fn))

acc = []
gyr = []
magn = []
DOF_time = np.zeros(len(DOF_data))

# split text file with two columns of data into data sets
# use on text file format: type 1, type 2
def splitData(raw, list_type1, list_type2):
	# this function may be useful in analysis scripts :)
	for i in raw:
		l = i.split(', ')
		list_type1.append(float(l[0]))
		list_type2.append(float(l[1]))
	return list_type1, list_type2

"""
extract data from 9DOF readout file for the corresponding experiment. Same deal.
"""

# first split each row of data to make list of lists  and time coordinates 
for i,n in zip(DOF_data, range(len(DOF_data))):
	l = i.split(';')
	acc.append(l[0])	# list of lists: each entry [dat_x, dat_y, dat_z]
	gyr.append(l[1])
	magn.append(l[2])
	DOF_time[n] = float(l[3])

# split up acceleration data, sort into x, y, z directions 
acc_x = np.zeros(len(acc))
acc_y = np.zeros(len(acc))
acc_z = np.zeros(len(acc))

for i,n in zip(acc, range(len(acc))):
	i = i[1:(len(i) - 1)] # get rid of brackets
	l = i.split(', ')
	acc_x[n] = l[0]
	acc_y[n] = l[1]
	acc_z[n] = l[2]

# sort gyroscopic data 
gyr_x = np.zeros(len(gyr))
gyr_y = np.zeros(len(gyr))
gyr_z = np.zeros(len(gyr))

for i,n in zip(gyr, range(len(gyr))):
	i = i[2:(len(i) - 1)] # get rid of brackets
	l = i.split(', ')
	gyr_x[n] = l[0]
	gyr_y[n] = l[1]
	gyr_z[n] = l[2]

# sort magnetic measurements
magn_x = np.zeros(len(magn))
magn_y = np.zeros(len(magn))
magn_z = np.zeros(len(magn))

for i,n in zip(magn, range(len(magn))):
	i = i[2:(len(i) - 1)] # get rid of brackets
	l = i.split(', ')
	magn_x[n] = l[0]
	magn_y[n] = l[1]
	magn_z[n] = l[2]

""" 
Get TOF I2C readout from same experiment.
"""

TOF_fn = 'TOF_Dat'+str(exp) +'.txt'
TOF_data = list(fr.file_readlines(TOF_fn))

d = []
TOF_time = []
d, TOF_time = splitData(TOF_data, d, TOF_time)	# use function i wrote earlier

"""
Calibrate time
Experiments likely did not start at exact same time
We will read out the start time, which is recorded in the data logs for each I2Cacqusition
We will use the frame of reference were t= 0 is at the start time if the TOF data acqusition
"""

TOF_log = fr.file_readlines('TOF_LOG.txt')	# extract start time of TOF experiment
for i in TOF_log:
	if i.find(TOF_fn) != -1:
		l = i.split(', ')
		TOF_t0 = float(l[1])
DOF_log = fr.file_readlines('9DOF_LOG.txt')

for i in DOF_log:	# extract start time of 9DOF experiment
	if i.find(DOF_fn) != -1:
		l = i.split(', ')
		DOF_t0 = float(l[1])
		crudeSPS =l[3]
		SPS =crudeSPS[4:len(crudeSPS)]

fixt = TOF_t0 - DOF_t0	# find the relative time coordinate of 9DOF start time to TOF start time 

for i,n in zip(DOF_time, range(len(DOF_time))):
	DOF_time[n] = i - fixt	# add fixt to each DOF to match with TOF coordinates


"""
Create functions that will allow the user to get specific values which are extracted by this file.

User needs to get familiar with this library to pull data appropriately

eg. note getAcc() returns three values in the order acc_x, acc_y, acc_z 
	so to pull acc_x and use it in an analysis script, use"
	import format_data
	acc_x, acc_y, acc_z = format_data.getAcc()

"""
def writeCSV():
	fout = "INT_Exp" + exp + ".csv"
	csv = open(fout, 'w+')
	header = "TOF time (sec) , d (mm) , 9DOF time (sec) , acc_x (m/s^2) , acc_y (m/s^2), acc_z (m/s^2), magn_x (gauss) , magn_y (gauss), magn_z (gauss_, gyr_x (radians/s), gyr_y (radians/s), gyr_z (radians/s)\n"
	csv.write(header)
	for a, b, c, dd, e, f, g, h, i, j, k, l in zip(TOF_time, d, DOF_time, acc_x,acc_y, acc_z, magn_x, magn_y, magn_z, gyr_x, gyr_y, gyr_z):
		try: 
			line = str(a) + ", " + str(b) + ", " + str(c) + ", " + str(dd) + ", " + str(e) + ", " + str(f) + ", " + str(g) + ", " + str(h) + ", " + str(i) + ", " + str(j) + ", " + str(k) + ", " + str(l) + '\n'
			csv.write(line)
		except ValueError:
			pass 
	csv.close()


def getAcc():
	return acc_x, acc_y, acc_z

def getGyr():
	return gyr_x, gyr_y, gyr_z

def get9DOF_time():
	return DOF_time

def getTOF_time():
	return TOF_time

def getMagn():
	return magn_x, magn_y, magn_z

def getDist():
	return d

def getSPS():
	return float(SPS)

def getExp():
	return exp

def getOut():
	return DOF_fn

