#! /usr/bin/env python
# -*- coding: utf-8 -*-

import random
from mpl_toolkits.mplot3d import Axes3D
from scipy.misc import comb
import matplotlib.pyplot as mpl
import numpy as np

from libmain import *
from libsubbytes import *
from libshiftrows import *
from libmixcolumns import *
from libkeyexpansion import *




def generateAleaBooleanFunction():
	"""Generate the Truth Table of a Boolean Function
	f(x): F_2^octetSize to F_2^octetSize
	Value of f(x) are random"""
	result = []
	random.seed()
	for i in xrange(2**octetSize):
		val = random.randint(0, 2**octetSize)
		result.append(int2bin(val))
	return result


def generateEqua():
#	tt = generateAleaBooleanFunction()
#	tt = generateSboxTruthTable()
	tt = generateInvSboxTruthTable()
	mt = generateMoebiusTransform(tt)
	equa = generateEquaMonomes(mt)
	return equa


def numberOfMonomes(equa):
	tab = []
	for i in xrange(len(equa)):
		result = [0, 0, 0, 0, 0, 0, 0, 0]
		listOfMonomes = equa[i].split('+')
		tabOfDegree = []
		for monome in listOfMonomes:
			degree = monome.split('x_')
			tabOfDegree.append(len(degree)-1)
		for degree in tabOfDegree:
			result[degree-1] += 1
		tab.append(result)
	return tab


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
	nvy = [octetSize+0.5 for i in xrange(octetSize)]
	nvz = [(0.5 * comb(octetSize, i+1)) for i in xrange(octetSize)]

	max = 0 # zscale definition
	for i in xrange(len(tab)):
		for j in xrange(len(tab[i])):
			if tab[i][j] > max:
				max = tab[i][j]

	xscale = [i for i in xrange(1, octetSize+1, 1)] # degree of monome
	yscale = [i for i in xrange(octetSize)] # bit number
	zscale = [i for i in xrange(0, max, 5)] # number of monome

	fig = mpl.figure(figsize=(8, 6), dpi=100) # fig definition -> figsize=(16, 12)
	ax = fig.add_subplot(111, projection='3d')

	for i in xrange(octetSize):
		ax.bar(xscale, tab[i], zs=i, zdir='y', align='center', color=rgb, alpha=1.0, edgecolor=rgbDark)
	ax.plot(nvx, nvy, zs=nvz, zdir='z', linewidth=4, color='r', marker='s', label='Loi normale', alpha=1.0)

	ax.set_xlabel('Degre des monomes')
	ax.set_xticks(xscale)
	ax.set_xticklabels(xscale, rotation=0, ha='center', va='center', size=8)

	ax.set_ylabel('Numero du bit')
	ax.set_yticks(yscale)
	ax.set_yticklabels(yscale, rotation=-90, ha='center', va='center', size=8)

	ax.set_zlabel('Nombre de monomes')
	ax.set_zticks(zscale)
	ax.set_zticklabels(zscale, rotation=0, ha='center', va='center', size=8)
	
	ax.legend(loc='lower left', prop={'size':8})
	ax.grid(True)

#	for degree in [10, 230, 300, 350]:
#		ax.view_init(4, degree)
#		extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
#		mpl.savefig('graph_'+str(degree)+'.png', dpi=100, bbox_inches=extent, pad_inches=0)
	mpl.show()


def displayTabMeanVariance(n):
	for d in xrange(n):
		e = 0.5 * comb(n, d+1)
		v = 0.25 * comb(n, d+1)
		print "n=%s\td=%s\tE=%s and V=%s" % (n, d+1, e, v)
	print


if __name__ == "__main__":
	displayTabMeanVariance(octetSize)
	equa = generateEqua()
#	for i in xrange(len(equa)):
#		print i, '\t', equa2sagemath(equa[i])
	tab = numberOfMonomes(equa)
	monomesGraph(tab)







