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
from libshiftrows import *
from libmixcolumns import *
from libkeyexpansion import *




def computeMean(n):
	result = []
	for d in xrange(n):
		result.append(0.5 * comb(n, d+1))
	return result


def countMonomes(tab):
	degree = [0, 0, 0, 0, 0, 0, 0, 0]
	for monome in tab:
		monome = monome.split('\t')[1]
		tmp = monome.count('1')
		degree[tmp] += 1
	return degree


def monomesGraph(tab):
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

	nvx = [i for i in xrange(octetSize)]
	nvy = [blockSize+1 for i in xrange(octetSize)]
	nvz = [(0.5 * comb(octetSize, i+1)) for i in xrange(octetSize)]

	max = 0 # zscale definition
	for i in xrange(len(tab)):
		for j in xrange(len(tab[i])):
			if tab[i][j] > max:
				max = tab[i][j]

	xscale = [i for i in xrange(1, octetSize+1, 1)] # degree of monome
	yscale = [i for i in xrange(0, blockSize, 15)] # bit number
	zscale = [i for i in xrange(0, max, 10)] # number of monome

	fig = mpl.figure(figsize=(8, 6), dpi=100) # fig definition -> figsize=(16, 12)
	ax = fig.add_subplot(111, projection='3d')

	for i in xrange(blockSize):
		ax.bar(xscale, tab[i], zs=i, zdir='y', align='center', color=rgb, alpha=1.0, edgecolor=rgbDark)
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

	ax.legend(loc='lower left', prop={'size':8})
	ax.grid(True)

#	for degree in [10, 230, 300, 350]:
#		ax.view_init(4, degree)
#		extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
#		mpl.savefig('graph_'+str(degree)+'.png', dpi=100, bbox_inches=extent, pad_inches=0)
	mpl.show()


def displayLatexTable(val, start, end):
	fname = (fileNameEnc if val == 'enc' else fileNameDec)
	for i in xrange(blockSize):
		f = fname + '%s.txt' % intToThreeChar(i)
		print "$%s$ &" % i, # numero of output bit
		tab = extractBlock(f, start, end)
		print "$%s$ &" % len(tab), # number of monomials
		d = countMonomes(tab)
		for m in xrange(len(d)):
			if m == len(d)-1:
				print "$%s$ \\tabularnewline\\hline" % d[m],
			else:
				print "$%s$ &" % d[m],
		print


def displayTableAES(val, start, end):
	expected = computeMean(8)
	aesDegrees = []
	fname = (fileNameEnc if val == 'enc' else fileNameDec)
	for i in xrange(blockSize):
		f = fname + '%s.txt' % intToThreeChar(i)
		print "Bit num: %s\t" % i,
		tab = extractBlock(f, start, end)
		print "Nombre de monômes: %s\t" % len(tab),
		d = countMonomes(tab)
		print "Degrees distribution: %s\t" % d,
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
#	displayLatexTable('dec', '## invSubBytes2', '## addRoundKey2')
	aes = displayTableAES('dec', '## Round2', '## addRoundKey2')
	mean = computeMean(8)
	chi2Test(aes, mean)
	computeStatDistance(aes, mean)
	monomesGraph(aes)






