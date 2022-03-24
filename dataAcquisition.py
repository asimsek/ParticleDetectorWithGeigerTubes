#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import datetime as dt
import matplotlib.pyplot as plt
from MCP3008 import MCP3008
from drawnow import *
from scipy.signal import find_peaks, savgol_filter


raw_adc = MCP3008()
x, y = list(), list()

ymin = -0.1
ymax = 5.0
xMax = 100
voltageThreshold = 1.5 ## Volt



plt.ion()
plt.style.use('dark_background')
fig=plt.figure()
def plotting():
	plt.title('Osciloscope')
	plt.grid(True)
	plt.ylabel('Voltage (V)', loc='top')
	plt.xlabel('a.u.', loc='right')
	plt.ylim(ymin, ymax)
	plt.plot(x, y, '.-', linewidth=1.5, label='channel #0') #, color='y'
	plt.legend(loc='upper right')
	plt.show()
	plt.pause(0.0001)



fooVoltArr, fooDateArr = list(), list()
def discriminator(voltage, signalDate):
	try:
		#if voltage < voltageThreshold and not fooVoltArr: voltage = 0.0; x.append(signalDate); y.append(voltage)
		if voltage > voltageThreshold or fooVoltArr: fooVoltArr.append(voltage); fooDateArr.append(signalDate)
		if voltage == 0.0 and fooVoltArr:
			#### Smoothing the signal!
			l = len(fooVoltArr)
			if (l % 2) == 0: l-=1
			y_filtered = savgol_filter(fooVoltArr, l, 5)
			####

			#### Always show the signal at the middle of the histogram!
			for i in range(0, int(xMax/4)): x.append(i); y.append(0.0)
			for j in range(0, len(fooVoltArr)): x.append(int(xMax/4)+j); y.append(y_filtered[j])
			for k in range(int(xMax/4)+len(fooVoltArr)+1, xMax): x.append(k); y.append(0.0)
			####

			#### Plotting and clearing lists & figure!
			plotting()
			del fooVoltArr[:]
			del fooDateArr[:]
			del x[:]
			del y[:]
			fig.clf()
	except:
		pass
	
	

def dataTake(ch=0):
	os.system('mkdir -p logs/')
	dateNow = dt.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
	print ("Start Date: %s" % (dateNow))
	outTextFile = 'logs/log_%s.txt' % (dateNow)
	print ("Data log File: %s" % (outTextFile))
	
	##### Start Data Taking
	with open(outTextFile, 'w') as f:
		dateC = -1
		try:
			while True:
				dateC += 1
				valueC = raw_adc.read( channel = ch ) / 1023.0 * 3.3
				
				### Signal-BG Discrimination
				discriminator(voltage = valueC, signalDate = dateC)
		except KeyboardInterrupt:
			pass


if __name__== "__main__":
	dataTake()
