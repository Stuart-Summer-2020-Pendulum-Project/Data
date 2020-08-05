#!/usr/bin/env python3
#
#

import numpy as np
import matplotlib.pyplot as plt
import file_readlines as fr

exp = str(input("\nInput experiment number for external measurements: "))
f = "LightDat" + exp + ".txt"
data = list(fr.file_readlines(f))

v = np.zeros(len(data))
time = np.zeros(len(data))

for i,n in zip(data, range(len(data))):
	l = i.split(', ')
	v[n] = l[0]
	time[n] = l[1]

def getExp():
	return exp

def getPot():
	return v

def getLightSensTime():
	return time

def writeCSV():
	fout = "EXT+Exo" + exp + ".csv"
	csv = open(fout, 'w+')
	header = "Time (sec), Light Intensity (mV)"
	csv.write(header)
	for i, j in zip(time, v):
		line = str(i) + ', ' + str(j)
		csv.write(line)
	csv.close()
