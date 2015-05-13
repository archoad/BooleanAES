#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as mpl
from scipy.misc import comb
from scipy.stats.mstats import chisquare
from scipy.stats import chisqprob
from scipy.stats import chi2_contingency
import numpy as np
from libmain import *
from libsubbytes import *
from libmixcolumns import *



def extractSubBytes(file):
	tmp = []
	flag = 0
	f = openFile(file)
	allLines = readFile(file)
	closeFile(f)
	for line in allLines:
		line = line.rstrip('\r\n')
		if line == '## subBytes': flag = 1
		if line == '## shiftRows': flag = 0
		if flag:
			if line[0] <> '#':
				tmp.append(line.split('\t')[1])
	return tmp


def extractMixColumns(file):
	tmp = []
	flag = 0
	f = openFile(file)
	allLines = readFile(file)
	closeFile(f)
	for line in allLines:
		line = line.rstrip('\r\n')
		if line == '## mixColumns': flag = 1
		if line == '## end': flag = 0
		if flag:
			if line[0] <> '#':
				tmp.append(line.split('\t')[1])
	return tmp


def extractRound(file):
	tmp = []
	flag = 0
	f = openFile(file)
	allLines = readFile(file)
	closeFile(f)
	for line in allLines:
		line = line.rstrip('\r\n')
		if line == '## Round': flag = 1
		if line == '## end': flag = 0
		if flag:
			if line[0] <> '#':
				tmp.append(line.split('\t')[1])
	return tmp


def countMonomes(tab):
	degree = [0, 0, 0, 0, 0, 0, 0, 0]
	for monome in tab:
		degree[monome.count('1')-1] += 1
	return degree


def monomesGraph(tab):
	rgb = [] #color definition
	np.random.seed()
	for i in xrange(blockSize):
		rgb.append([np.random.random(), np.random.random()])

	max = 0 # zscale definition
	for i in xrange(blockSize):
		for j in xrange(len(tab[i])):
			if tab[i][j] > max:
				max = tab[i][j]

	nvx = [i for i in xrange(1, 9, 1)]
	nvy = [blockSize+1 for i in xrange(1, 9, 1)]
	nvz = [(0.5 * comb(8, i+1)) for i in xrange(8)]

	xscale = [i for i in xrange(1, 9, 1)] # degree of monome
	yscale = [i for i in xrange(0, blockSize, 15)] # bit number
	zscale = [i for i in xrange(0, max, 2)] # number of monome

	fig = mpl.figure() # fig definition
	ax = fig.add_subplot(111, projection='3d')

	for i in xrange(blockSize):
		cs = []
		for j in xrange(len(tab[i])):
			cs.append( (1-((i+0.1)/float(4*blockSize)), rgb[j][1], rgb[j][0]) )
		ax.bar(xscale, tab[i], zs=i, zdir='y', align='center', color=cs, alpha=0.8)
	ax.plot(nvx, nvy, zs=nvz, zdir='z', linewidth=4, color='r', marker='s', label='Normal distribution', alpha=1.0)

	ax.set_xlabel('degree of monome')
	ax.set_xticks(xscale)
	ax.set_xticklabels(xscale, rotation=0, ha='center', va='center', size=8)

	ax.set_ylabel('bit number')
	ax.set_yticks(yscale)
	ax.set_yticklabels(yscale, rotation=-90, ha='center', va='center', size=8)

	ax.set_zlabel('number of monome')
	ax.set_zticks(zscale)
	ax.set_zticklabels(zscale, rotation=0, ha='center', va='center', size=8)

	ax.legend(loc='lower left', prop={'size':8})

	mpl.grid(True)
	for degree in [10, 230, 300, 350]:
		ax.view_init(4, degree)
		extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
		mpl.savefig('graph_'+str(degree)+'.png', dpi=90, bbox_inches=extent, pad_inches=0)
	mpl.show()


def displayLatexTable():
	for i in xrange(blockSize):
		print "$%s$ &" % i, # numero of output bit
		tab = extractRound('f_%s.txt' % (intToThreeChar(i)))
		print "$%s$ &" % len(tab), # number of monomials
		d = countMonomes(tab)
		for m in xrange(len(d)):
			if m == len(d)-1:
				print "$%s$ \\tabularnewline\\hline" % d[m],
			else:
				print "$%s$ &" % d[m],
		print


def computeMean(n):
	result = []
	for d in xrange(n):
		result.append(0.5 * comb(n, d+1))
	return result


def displayTableAES():
	expected = computeMean(8)
	aesDegrees = []
	for i in xrange(blockSize):
		print "Bit num: %s ->\t" % i,
#		tab = extractSubBytes('f_%s.txt' % (intToThreeChar(i)))
#		tab = extractMixColumns('f_%s.txt' % (intToThreeChar(i)))
		tab = extractRound('f_%s.txt' % (intToThreeChar(i)))
		print "Nombre de monômes: %s ->\t" % len(tab),
		d = countMonomes(tab)
		print "Degrees distribution: %s" % d, len(d),
		print "Expected: %s" % expected
		aesDegrees.append(d)
	return aesDegrees


def computeStatDistance(aes, mean):
	distance = [0 for i in xrange(len(mean))]
	result = []
	for bit in xrange(len(aes)):
		tmp = []
		for i in xrange(len(mean)):
			tmp.append( pow((aes[bit][i] - mean[i]), 2) / mean[i] )
		result.append(tmp)
	for i in xrange(len(mean)):
		for j in xrange(len(aes)):
			distance[i] += result[j][i]
	print distance


def chi2Test(aes, mean):
	# info: http://vassarstats.net/textbook/ch8pt1.html
	tmp = []
	for i in xrange(blockSize):
		tmp.append(mean)
	for d in xrange(len(mean)):
		expected=np.zeros(blockSize)
		observed=np.zeros(blockSize)
		for i in xrange(blockSize):
			expected[i] = tmp[i][d]
			observed[i] = aes[i][d]
		chi = chisquare(observed, expected, ddof=7)
		chi = np.around(chi, decimals=2)
		print "Chi2=%s,\tp-value=%s,\tprobability of null hypothesis: %s" %(chi[0], chi[1], chisqprob(chi[0], 7))
		# contingency table
#		chi2, pv, dof, ex = chi2_contingency(np.array([observed, expected]), correction=False)
#		print "Chi2=%s,\tp-value=%s,\tdf: %s" %(chi2, pv, dof)


if __name__ == "__main__":
#	displayLatexTable()
	aes = displayTableAES()
	mean = computeMean(8)
	chi2Test(aes, mean)
	computeStatDistance(aes, mean)
	monomesGraph(aes)








