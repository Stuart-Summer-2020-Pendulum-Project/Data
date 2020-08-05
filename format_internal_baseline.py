#!/usr/bin/env python3

# this script will fit the TOF data and find corresponding theta values, calculate the period, and calculate gravity 

import numpy as np
import file_readlines as fr

### get user input 
exp = input("Enter the experiment number of the control, which will be used for baseline data: ")

### Get 9DOF Data
DOF_fn = str('9DOF_Dat'+ str(exp) + '.txt')
DOF_data = list(fr.file_readlines(DOF_fn))

def getOut():
	return DOF_fn
acc = []
gyr = []
magn = []
DOF_time = np.zeros(len(DOF_data))

for i,n in zip(DOF_data, range(len(DOF_data))):
	l = i.split(';')
	acc.append(l[0])
	gyr.append(l[1])
	magn.append(l[2])
	DOF_time[n] = float(l[3])


acc_x = np.zeros(len(acc))
acc_y = np.zeros(len(acc))
acc_z = np.zeros(len(acc))

for i,n in zip(acc, range(len(acc))):
	i = i[1:(len(i) - 1)] # get rid of brackets
	l = i.split(', ')
	acc_x[n] = l[0]
	acc_y[n] = l[1]
	acc_z[n] = l[2]


gyr_x = np.zeros(len(gyr))
gyr_y = np.zeros(len(gyr))
gyr_z = np.zeros(len(gyr))

for i,n in zip(gyr, range(len(gyr))):
	i = i[2:(len(i) - 1)] # get rid of brackets
	l = i.split(', ')
	gyr_x[n] = l[0]
	gyr_y[n] = l[1]
	gyr_z[n] = l[2]

magn_x = np.zeros(len(magn))
magn_y = np.zeros(len(magn))
magn_z = np.zeros(len(magn))

for i,n in zip(magn, range(len(magn))):
	i = i[2:(len(i) - 1)] # get rid of brackets
	l = i.split(', ')
	magn_x[n] = l[0]
	magn_y[n] = l[1]
	magn_z[n] = l[2]

### get TOF data
TOF_fn = 'TOF_Dat'+str(exp) +'.txt'
TOF_data = list(fr.file_readlines(TOF_fn))

d = np.zeros(len(TOF_data))
TOF_time = np.zeros(len(TOF_data))

for i,n in zip(TOF_data, range(len(TOF_data))):
	l = i.split(', ')
	d[n] = l[0]
	TOF_time[n] = l[1]

#correct(d)

### correct time 
TOF_log = fr.file_readlines('TOF_LOG.txt')
for i in TOF_log:
	if i.find(TOF_fn) != -1:
		l = i.split(', ')
		TOF_t0 = float(l[1])
DOF_log = fr.file_readlines('9DOF_LOG.txt')

for i in DOF_log:
	if i.find(DOF_fn) != -1:
		l = i.split(', ')
		DOF_t0 = float(l[1])
		crudeSPS =l[3]
		SPS =crudeSPS[4:len(crudeSPS)]

fixt = TOF_t0 - DOF_t0

def avg(dat):
	return sum(dat)/len(dat)

for i,n in zip(DOF_time, range(len(DOF_time))):
	DOF_time[n] = i + fixt

def BaseAcc():
	return avg(acc_x), avg(acc_y), avg(acc_z)

def BaseGyr():
	return avg(gyr_x), avg(gyr_y), avg(gyr_z)

def Base9DOF_time():
	return DOF_time

def BaseTOF_time():
	return TOF_time

def BaseMagn():
	return avg(magn_x), avg(magn_y), avg(magn_z)

def BaseDist():
	return avg(d)

def BaseSPS():
	return SPS

def BaseExp():
	return exp
