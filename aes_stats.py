#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import sys
import math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as mpl
from scipy import misc
from scipy import stats
import numpy as np
from pycallgraph import PyCallGraph
from pycallgraph import Config
from pycallgraph.output import GraphvizOutput

from libmain import *
from libsubbytes import *
from libshiftrows import *
from libmixcolumns import *
from libkeyexpansion import *
from libequaenc import *
from libequadec import *




rgb = [ # source http://colors.findthedata.com/saved_search/Pastel-Colors
	[119.0/255.0, 190.0/255.0, 119.0/255.0], # pastel green
	[244.0/255.0, 154.0/255.0, 194.0/255.0], # pastel magenta
	[255.0/255.0, 179.0/255.0, 71.0/255.0], # pastel orange
	[222.0/255.0, 165.0/255.0, 164.0/255.0], # pastel pink
	[207.0/255.0, 207.0/255.0, 196.0/255.0], # pastel gray
	[194.0/255.0, 59.0/255.0, 34.0/255.0], # dark pastel red
	[119.0/255.0, 158.0/255.0, 203.0/255.0], # dark pastel blue
	[100.0/255.0, 20.0/255.0, 100.0/255.0] # light pastel purple
]

rgbDark = ([[item[0]-0.07, item[1]-0.07, item[2]-0.07] for item in rgb])




def generateChi2Table(dofs, dofe):
	#source: http://www.reid.ai/2012/09/chi-squared-distribution-table-with.html
	printColor("### Calculating chi2 table", GREEN)
	#stand deviations to calculate
	sigma = [
		np.sqrt(stats.chi2.ppf(0.95, 1)),
		np.sqrt(stats.chi2.ppf(0.99, 1)),
		np.sqrt(stats.chi2.ppf(0.999, 1))
	]
	#confidence intervals these sigmas represent:
	conf_int = [ stats.chi2.cdf(s**2, 1) for s in sigma ]
	#degrees of freedom to calculate
	dof = range(dofs, dofe)
	for ci in conf_int:
		print("p-value\t%1.4f" % (1-ci))
	for d in dof:
		chi_squared = [ stats.chi2.ppf(ci, d) for ci in conf_int ]
		for c in chi_squared:
			print("chi2(k=%d)\t%1.2f" % (d, c))


def computeMean(n):
	result = []
	for d in range(n+1):
		result.append(0.5 * misc.comb(n, d))
	return result


def computeVariance(n):
	result = []
	for d in range(n+1):
		result.append(0.25 * misc.comb(n, d))
	return result


def displayTabMeanVariance(n):
	for d in range(n+1):
		e = 0.5 * misc.comb(n, d)
		v = 0.25 * misc.comb(n, d)
		print("n=%s\td=%s\tE=%s\tV=%s" % (n, d, e, v))
	print


def countMonomes(tab):
	degree = [0 for i in range(octetSize+1)]
	for monome in tab:
		m = monome.split('\t')[1]
		degree[m.count('1')] += 1
	return degree


def distributionBitsGraph(y, name, display=False):
	w = 0.6
	x = np.arange(blockSize)
	low = min(y)
	high = max(y)
	fig = mpl.figure(figsize=(8, 6), dpi=100) # fig definition -> figsize=(16, 12) figsize=(8, 6)
	ax = fig.add_subplot(111)
	ax.bar(x, y, w, align='center', color=rgb, edgecolor=rgbDark)
	ax.set_xlabel('Numero du bit')
	xscale = [i for i in range(0, blockSize+7, 8)]
	ax.set_xticks(xscale)
	for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
		item.set_fontsize(8)
	ax.grid(True)
	mpl.xlim([-2, blockSize+1])
	mpl.ylim([math.ceil(low-0.5*(high-low)), math.ceil(high+0.5*(high-low))])
	if display:
		mpl.show()
	else:
		mpl.savefig('graph_bit_distrib_'+name+'.png', dpi=160)


def distribution2BitsGraph(tab, name, display=False):
	data = np.asarray(tab)
	gap = np.ceil((np.max(data) - np.min(data)) / 8.).astype(int)
	fig = mpl.figure(figsize=(8, 6), dpi=100)
	ax = Axes3D(fig)
	xpos = np.arange(0,blockSize,1)
	ypos = np.arange(0,blockSize,1)
	xpos, ypos = np.meshgrid(xpos+0.25, ypos+0.25)
	xpos = xpos.flatten()
	ypos = ypos.flatten()
	zpos = np.zeros(blockSize*blockSize)
	dx = 0.5 * np.ones_like(zpos)
	dy = dx.copy()
	dz = data.flatten()
	for s in range(blockSize**2):
		for c in range(len(rgb)):
			if (dz[s]>=c*gap) & (dz[s] < (c+1)*gap): col = c
		ax.bar3d(xpos[s], ypos[s], zpos[s], dx[s], dy[s], dz[s], color=rgb[col], alpha=0.6, edgecolor=rgbDark[col])
	ax.set_xlabel("Numero du premier bit")
	ax.set_ylabel("Numero du deuxieme bit")
	ax.set_zlabel("Nombre d'occurences")
	for item in ([ax.xaxis.label, ax.yaxis.label, ax.zaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()) + ax.get_zticklabels():
		item.set_fontsize(8)
	ax.grid(True)
	ax.view_init(azim=30, elev=8)
	xyPos = [i+0.5 for i in range(0, blockSize, 8)]
	xyLab = [i for i in range(0, blockSize, 8)]
	mpl.xticks(xyPos, xyLab)
	mpl.yticks(xyPos, xyLab)
	if display:
		mpl.show()
	else:
		mpl.savefig('graph_2bit_distrib_'+name+'.png', dpi=160)


def distributionMonomeGraph(tabEnc, tabDec, display=False):
	fig = mpl.figure(figsize=(8, 6), dpi=100) # fig definition -> figsize=(16, 12) figsize=(8, 6)
	ax = fig.add_subplot(111)
	ax.plot(tabEnc, marker='.', label='Chiffrement', color='tan')
	ax.plot(tabDec, marker='.', label='Dechiffrement', color='violet')
	#mpl.axis([0, 127, min(tabEnc)-100, max(tabEnc)+100])
	#ax.legend([e, d], ["Cipher", "Decipher"])
	ax.grid(True)
	ax.set_xlabel('Numero du bit')
	ax.set_ylabel('Nombre de monomes')
	xscale = [i for i in range(0, blockSize+7, 8)]
	ax.set_xticks(xscale)
	for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
		item.set_fontsize(8)
	ax.legend(bbox_to_anchor=(1.1, -0.03), prop={'size':8})
	if display:
		mpl.show()
	else:
		mpl.savefig('graph_monom_distrib.png', dpi=160)


def monomesGraph(tab, mode, display=False):
	nvx = [i for i in range(octetSize)]
	nvy = [blockSize+1 for i in range(octetSize)]
	nvz = [(0.5 * misc.comb(octetSize, i+1)) for i in range(octetSize)]

	max = 0 # zscale definition
	for i in range(len(tab)):
		for j in range(len(tab[i])):
			if tab[i][j] > max:
				max = tab[i][j]

	xscale = [i for i in range(0, octetSize+1, 1)] # degree of monome
	yscale = [i for i in range(0, blockSize, 15)] # bit number
	zscale = [i for i in range(0, max, int(max/10))] # number of monome


	fig = mpl.figure(figsize=(8, 6), dpi=100) # fig definition -> figsize=(16, 12) figsize=(8, 6)
	ax = fig.add_subplot(111, projection='3d')

	for i in range(blockSize):
		ax.bar(xscale, tab[i-1], zs=i, zdir='y', align='center', color=rgb, alpha=1.0, edgecolor=rgbDark)
	ax.plot(nvx, nvy, zs=nvz, zdir='z', linewidth=4, color='r', marker='s', label='Loi normale', alpha=1.0)

	ax.set_xlabel('Degre des monomes')
	ax.set_xticks(xscale)
	ax.set_xticklabels(xscale, rotation=0, ha='center', va='center', size=6)

	ax.set_ylabel('Numero du bit')
	ax.set_yticks(yscale)
	ax.set_yticklabels(yscale, rotation=-90, ha='center', va='center', size=6)

	ax.set_zlabel('Nombre de monomes')
	ax.set_zticks(zscale)
	ax.set_zticklabels(zscale, rotation=0, ha='center', va='center', size=6)

	for item in ([ax.xaxis.label, ax.yaxis.label, ax.zaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()) + ax.get_zticklabels():
		item.set_fontsize(8)

	ax.legend(loc='lower left', prop={'size':8})
	ax.grid(True)
	for degree in [10, 230, 300, 350]:
		ax.view_init(4, degree)
		extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
		mpl.savefig('graph_'+str(degree)+'_'+mode+'.png', dpi=160, bbox_inches=extent, pad_inches=0)
	if display:
		mpl.show()



def displayLatexTable(val, start, end):
	fname = (fileNameEnc if val == 'enc' else fileNameDec)
	for i in range(blockSize):
		f = fname + '%s.txt' % intToThreeChar(i)
		print("$%s$ &" % i), # numero of output bit
		tab = extractBlock(f, start, end)
		print("$%s$ &" % len(tab)), # number of monomials
		d = countMonomes(tab)
		for m in range(len(d)):
			if m == len(d)-1:
				print("$%s$ \\tabularnewline\\hline" % d[m]),
			else:
				print("$%s$ &" % d[m]),
		print


def displayTableAES(val, start, end):
	aesDegree = []
	degreeSum = [0 for i in range(octetSize+1)]
	fname = (fileNameEnc if val == 'enc' else fileNameDec)
	for i in range(blockSize):
		f = fname + '%s.txt' % intToThreeChar(i)
		print("Bit number: %s\t" % i),
		tab = extractBlock(f, start, end)
		print("Number of monomials: %s\t" % len(tab)),
		d = countMonomes(tab)
		print("Degrees distribution: %s\t" % d)
		aesDegree.append(d)
	for i in range(blockSize):
		for j in range(octetSize+1):
			degreeSum[j] += aesDegree[i][j]
	print("Sum of degrees: %s" % degreeSum)
	return aesDegree


def computeStatDistance(aes, mean):
	printColor("### Calculating chi2 manually", GREEN)
	distance = [0 for i in range(len(mean))]
	result = []
	for bit in range(len(aes)):
		tmp = []
		for i in range(len(mean)):
			tmp.append( pow((aes[bit][i] - mean[i]), 2) / mean[i] )
		result.append(tmp)
	for i in range(len(mean)):
		for j in range(len(aes)):
			distance[i] += result[j][i]
	for i in range(len(mean)):
		distance[i] = np.round(distance[i], decimals=2)
		print("Chi2=%s" % distance[i])


def chi2Test(degree, mean):
	# info: http://vassarstats.net/textbook/ch8pt1.html
	# info: http://hamelg.blogspot.fr/2015/11/python-for-data-analysis-part-25-chi.html
	printColor("### Calculating chi2 with scipy library", GREEN)
	print(mean)
	tmp = [mean for i in range(blockSize)]
	for d in range(len(mean)):
		expected =np.zeros(blockSize)
		observed =np.zeros(blockSize)
		for i in range(blockSize):
			expected[i] = tmp[i][d]
			observed[i] = float(degree[i][d])
		#print(observed, np.sum(observed))
		#print(expected, np.sum(expected))
		(statistic, pvalue) = stats.chisquare(f_obs=observed, f_exp=expected)
		statistic = np.around(statistic, decimals=2)
		pvalue = np.around(pvalue, decimals=8)
		print("Chi2=%s,\tp-value=%s" % (statistic, pvalue))


def countAllMonomes(allLines):
	tmp = []
	for i in range(len(allLines)):
		if not allLines[i].startswith('##'):
			tmp.append(allLines[i])
	return countMonomes(tmp)


def monomesDistribution(equa, n):
	printColor("### Calculation of monomes disribution (grouped by 2)", MAGENTA)
	numMonom = [[0 for i in range(n)] for i in range(n)]
	for num in range(n):
		tmp = equa[num].split('+')
		for mon in tmp:
			monom = mon.split('x_')
			del monom[0]
			l = len(monom)
			if l >1:
				for r in range(0, l-1, 1):
					numMonom[int(monom[r])][int(monom[r+1])] += 1
	for item in numMonom:
		print(item)
	return numMonom


def someTests(size):
	displayTabMeanVariance(size)
	print(computeMean(size))
	print(computeVariance(size))


def generateGraphCode():
	graphviz = GraphvizOutput(output_file='graph_code.png')
	with PyCallGraph(output=graphviz, config=Config(groups=False)):
		subBytes()
		#invSubBytes()
		#shiftRows()
		#invShiftRows()
		#mixColumns()
		#invMixColumns()
		#generateWord(4)
		#generateWord(5)
		#generateWord(6)
		#generateWord(7)
		#generateEncFullFiles()


def roundFunctionsTest():
	testAESdirectory()
	generateEncStepsFiles()
	degree = displayTableAES('enc', '## subBytes0', '## shiftRows0') # subbytes function
	mean = [computeMean(8)[i] for i in range(octetSize+1)]
	chi2Test(degree, mean)
	computeStatDistance(degree, mean)
	generateChi2Table(127, 128)
	monomesGraph(degree, 'enc', display=False)


def roundTest(mode):
	testAESdirectory()
	(generateEncFullFiles() if mode == 'enc' else generateDecFullFiles())
	fname = (fileNameEnc if mode == 'enc' else fileNameDec)
	start = ('## Round0' if mode == 'enc' else '## Round9')
	end = ('## addRoundKey1' if mode == 'enc' else '## addRoundKey9')
	degree = displayTableAES(mode, start, end) # round
	mean = [computeMean(8)[i] for i in range(octetSize+1)]
	chi2Test(degree, mean)
	computeStatDistance(degree, mean)
	generateChi2Table(127, 128)
	monomesGraph(degree, mode, display=False)


def roundKeyTest():
	testAESdirectory()
	generateEncFullFiles()
	degree = displayTableAES('enc', '## addRoundKey2', '## Round2') # round key
	mean = [computeMean(8)[i] for i in range(octetSize+1)]
	chi2Test(degree, mean)
	computeStatDistance(degree, mean)
	generateChi2Table(127, 128)
	monomesGraph(degree, 'enc', display=True)


def fullEquaCombinatoryAnalysis():
	testAESdirectory()
	generateEncFullFiles()
	generateDecFullFiles()
	resultEnc = []
	resultDec = []
	nbMonomEnc = []
	nbMonomDec = []
	for bit in range(blockSize):
		fileEnc = fileNameEnc+'%s.txt' % intToThreeChar(bit)
		fileDec = fileNameDec+'%s.txt' % intToThreeChar(bit)
		allLinesEnc = readFile(fileEnc)
		allLinesDec = readFile(fileDec)
		numMonomE = len(allLinesEnc)
		numMonomD = len(allLinesDec)
		resultEnc.append(countAllMonomes(allLinesEnc))
		resultDec.append(countAllMonomes(allLinesDec))
		nbMonomEnc.append(numMonomE)
		nbMonomDec.append(numMonomD)
		print("bit number: %d" % (bit), numMonomE, resultEnc[bit], numMonomD, resultDec[bit])
	print('\r')
	distributionMonomeGraph(nbMonomEnc, nbMonomDec, display=False)


def oneBitDistribution(mode):
	"""Compute the use of each bit in the Boolean equations
	This function returns a 128 cases tab which details the number of time
	the bits b1...b128 appears in the equation"""
	numMonom = [0 for i in range(blockSize)]
	testAESdirectory()
	(generateEncFullFiles() if mode == 'enc' else generateDecFullFiles())
	fname = (fileNameEnc if mode == 'enc' else fileNameDec)
	start = ('## Round0' if mode == 'enc' else '## Round9')
	end = ('## addRoundKey1' if mode == 'enc' else '## addRoundKey9')
	for i in range(blockSize):
		f = fname + '%s.txt' % intToThreeChar(i)
		tab = extractBlock(f, start, end)
		for mon in tab:
			tmp = mon.split('\t')[1]
			for j in range(blockSize):
				if tmp[j] == '1':
					numMonom[j] += 1
	print(numMonom)
	distributionBitsGraph(numMonom, mode, display=False)


def twoBitDistribution(mode):
	if (mode == 'enc'):
		equa = generateRoundEncEqua(subBytes(), shiftRows(), mixColumns())
	if (mode == 'dec'):
		equa = generateRoundDecEqua(invSubBytes(), invShiftRows())
	if (mode == 'key'):
		equa = generateKn(generateWord(4), generateWord(5), generateWord(6), generateWord(7))
	distrib = monomesDistribution(equa, 128)
	distribution2BitsGraph(distrib, mode, display=False)




if __name__ == "__main__":
	print(sys.version)
	#someTests(octetSize)
	#generateGraphCode()
	#roundFunctionsTest()
	#roundTest('enc')
	#roundKeyTest()
	#fullEquaCombinatoryAnalysis()
	#oneBitDistribution('enc')
	twoBitDistribution('key')





#Rassembler tous les monômes
#Compter l'utilisation des monômes unitairement, par couple, par trinôme, ...
#Seuls 32 bits sont utilisés par equation
