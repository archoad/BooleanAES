#! /usr/bin/env python
# -*- coding: utf-8 -*-

import random
from libminiaes import *
from mpl_toolkits.mplot3d import Axes3D
from scipy.misc import comb
import matplotlib.pyplot as mpl
import numpy as np




def numberOfMonomes(mt):
	tab = []
	for i in xrange(blockSize):
		equa = definesMonomeBlock(mt[i])
#		print equaToLatex(equa)
		print 'Bit number %s --> ' % (i),
		result = {}
		for j in xrange(blockSize):
			result[j] = 0
		listOfMonomes = equa.split('+')
		tabOfDegree = []
		for monome in listOfMonomes:
			degree = monome.split('x')
			tabOfDegree.append(len(degree)-1)
		for degree in tabOfDegree:
			if degree<>blockSize:
				result[degree] += 1
		for d in xrange(blockSize):
			print "%s &" % (result[d]),
		print
		tab.append(result.values())
	return tab


def monomesGraph(tab):
	rgb = [] #color definition
	for i in xrange(blockSize):
		rgb.append([np.random.random(), np.random.random()])

	max = 0 # zscale definition
	for i in xrange(blockSize):
		for j in xrange(len(tab[i])):
			if tab[i][j] > max:
				max = tab[i][j]
	xscale = [i for i in xrange(1, blockSize+1, 1)] # degree of monome
	yscale = [i for i in xrange(0, blockSize, 1)] # bit number
	zscale = [i for i in xrange(0, max, 10)] # number of monome

	fig = mpl.figure() # fig definition
	ax = fig.add_subplot(111, projection='3d')

	for i in xrange(blockSize):
		cs = []
		for j in xrange(len(tab[i])):
			cs.append( (rgb[j][0], 1-(i/float(2*blockSize)), rgb[j][1]) )
		ax.bar(xscale, tab[i], zs=i, zdir='y',  align='center', color=cs, alpha=0.80)

	ax.set_xlabel('degree of monome')
	ax.set_xticks(xscale)
	ax.set_xticklabels(xscale, rotation=0, ha='center', va='center', size=8)

	ax.set_ylabel('bit number')
	ax.set_yticks(yscale)
	ax.set_yticklabels(yscale, rotation=-90, ha='center', va='center', size=8)

	ax.set_zlabel('number of monome')
	ax.set_zticks(zscale)
	ax.set_zticklabels(zscale, rotation=0, ha='center', va='center', size=8)

	mpl.grid(True)
	for degree in [230, 300]:
		ax.view_init(4, degree)
		extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
		mpl.savefig('graph_'+str(degree)+'.png', dpi=90, bbox_inches=extent, pad_inches=0)
	mpl.show()




if __name__ == "__main__":
#	(k0, k1, k2) = generateRoundsKeysTruthTable()
	r1 = generateRoundOneTruthTable()
#	r2 = generateRoundTwoTruthTable()
#	tt = generateNibbleSubTruthTable()
#	tt = generateShiftRowTruthTable()
#	tt = generateMixColumnsTruthTable()
	mt = generateMoebiusTransform(r1)
	tab = numberOfMonomes(mt)
	monomesGraph(tab)






