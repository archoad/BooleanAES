#! /usr/bin/env python
# -*- coding: utf-8 -*-

import random
from mpl_toolkits.mplot3d import Axes3D
from scipy.misc import comb
import matplotlib.pyplot as mpl
import numpy as np

blockSize = 8




def xorTab(t1, t2):
	"""Takes two tabs t1 and t2 of same lengths and returns t1 XOR t2."""
	result = ''
	for i in xrange(len(t1)):
		result += str(int(t1[i]) ^ int(t2[i]))
	return result


def intToBinBlock(i):
	"""Returns the string of the blockSize bits representation of integer i."""
	tmp = ""
	i = bin(i).lstrip('0b')
	for cpt in xrange(blockSize-len(i)):
		tmp += '0'
	tmp = tmp + i
	return tmp


def definesMonomeBlock(mt):
	"""Takes a moebius transform table and calulates corresponding monome.
	Scale is for block of blockSize bits"""
	tab = []
	equa = ''
	for i in xrange(2**blockSize):
		if mt[i] == '1':
			tmp = intToBinBlock(i)
			if i == 0:
				tab.append('1') # constant
			else:
				monome = ''
				for bit in xrange(blockSize):
					if tmp[bit] == '1':
						monome += 'x' + str(bit+1)
				tab.append(monome)
		else:
			tab.append('\t')
	for i in xrange(2**blockSize):
		if tab[i] <> '\t':
			equa += tab[i] + '+'
	return(equa.rstrip('+'))


def moebiusTransform(tab):
	"""Takes a tab and return tab[0 : len(tab)/2], tab[0 : len(tab)/2] ^ tab[len(tab)/2 : len(tab)]."""
	if len(tab) == 1:
		return tab
	else:
		t1 = tab[0 : len(tab)/2]
		t2 = tab[len(tab)/2 : len(tab)]
		t2 = xorTab(t1, t2)
		t1 = moebiusTransform(t1)
		t2 = moebiusTransform(t2)
		t1 += t2
		return t1


def generateMoebiusTransform(tab):
	"""Creates blockSize strings, each containing the result of Moebius
	Transform for a boolean function of tab. The result is a tab of blockSize
	cases each one containing 2**blockSize bits. Each case describe a bit of the function"""
	result = []
	for i in xrange(blockSize):
		tmp = ''
		for block in tab:
			tmp += block[i]
		result.append(moebiusTransform(tmp))
	return result


def generateBooleanFunction():
	"""Generate the Truth Table of a Boolean Function
	f(x): F_2^blockSize to F_2^blockSize
	Value of f(x) are random"""
	result = []
	random.seed()
	vals = []
	for i in xrange(blockSize):
		vals.append(random.randint(0, 2**blockSize))
	for i in xrange(2**blockSize):
		tmp = random.randint(0, (blockSize-1))
		result.append(intToBinBlock(vals[tmp]))
	return result


def numberOfMonomes(tt):
	mt = generateMoebiusTransform(tt)
	tab = []
	for i in xrange(blockSize):
		equa = definesMonomeBlock(mt[i])
		print 'Bit number %s' % (i)
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
		print result
		tab.append(result.values())
	return tab


def monomesGraph(tab):
	rgb = [] #color definition
	np.random.seed()
	for i in xrange(blockSize):
		rgb.append([np.random.random(), np.random.random()])

	nvx = [i for i in xrange(1, blockSize+1, 1)]
	nvy = [ blockSize+0.5 for i in xrange(0, blockSize, 1)]
	nvz = [(0.5 * comb(blockSize, i)) for i in xrange(1, blockSize+1, 1)]

	max = 0 # zscale definition
	for i in xrange(blockSize):
		for j in xrange(len(tab[i])):
			if tab[i][j] > max:
				max = tab[i][j]
	xscale = [i for i in xrange(1, blockSize+1, 1)] # degree of monome
	yscale = [i for i in xrange(0, blockSize, 1)] # bit number
	if blockSize <= 8:
		zscale = [i for i in xrange(0, max, 5)] # number of monome
	else:
		zscale = [i for i in xrange(0, max, (((max/blockSize)/10)*10))] # number of monome

	fig = mpl.figure() # fig definition
	ax = fig.add_subplot(111, projection='3d')

	for i in xrange(blockSize):
		cs = []
		for j in xrange(len(tab[i])):
			cs.append( (1-((i+0.1)/float(4*blockSize)), rgb[j][0], rgb[j][1]) )
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
	for degree in [230, 300]:
		ax.view_init(4, degree)
		extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
		mpl.savefig('graph_'+str(degree)+'.png', dpi=90, bbox_inches=extent, pad_inches=0)
	mpl.show()


def displayTabMeanVariance(n):
	for d in xrange(n):
		e = 0.5 * comb(n, d+1)
		v = 0.25 * comb(n, d+1)
		print "n=%s\td=%s\tE=%s and V=%s" % (n, d+1, e, v)
	print


if __name__ == "__main__":
	displayTabMeanVariance(8)
	tt = generateBooleanFunction()
	tab = numberOfMonomes(tt)
	monomesGraph(tab)







