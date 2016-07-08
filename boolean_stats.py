#! /usr/bin/env python
# -*- coding: utf-8 -*-

import random
from mpl_toolkits.mplot3d import Axes3D
from scipy.misc import comb
import matplotlib.pyplot as mpl
import numpy as np


BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(30, 38)


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


def printColor(string, color=RED):
	print('\033[1;%dm%s\033[0m' % (color, string))


def int2nsizeBin(i, n):
	"""Returns the string of the 8 bits representation of integer i.
	usage: int2bin(255, 8) --> 11111111"""
	tmp = ""
	i = bin(i).lstrip('0b')
	for cpt in range(n-len(i)):
		tmp += '0'
	tmp = tmp + i
	return tmp


def xorTab(t1, t2):
	"""Takes two tabs t1 and t2 of same lengths and returns t1 XOR t2."""
	result = ''
	for i in range(len(t1)):
		result += str(int(t1[i]) ^ int(t2[i]))
	return result


def moebiusTransform(tab):
	"""Takes a tab and return tab[0 : len(tab)/2], tab[0 : len(tab)/2] ^ tab[len(tab)/2 : len(tab)].
	usage: moebiusTransform(1010011101010100) --> [1100101110001010]"""
	if len(tab) == 1:
		return tab
	else:
		t1 = tab[0 : int(len(tab)/2)]
		t2 = tab[int(len(tab)/2) : len(tab)]
		t2 = xorTab(t1, t2)
		t1 = moebiusTransform(t1)
		t2 = moebiusTransform(t2)
		t1 += t2
		return t1


def generateMoebiusTransform(tt, n):
	"""Creates n sized strings, each containing the result of Moebius
	transform for a boolean function of tab. The result is a tab of length n
	cases each one containing 2**n bits. Each case describe a bit of the function"""
	printColor("### Calculation of Mobius transform", MAGENTA)
	result = []
	for i in range(n):
		tmp = ''
		for block in tt:
			tmp += block[i]
		result.append(moebiusTransform(tmp))
	return result


def bin2NsizeMonome(b, n):
	"""Return the monomes corresponding to the binary.
	usage: bin2monome(00110001, 8) = x_2+x_3+x_7"""
	result = ''
	for i in range(n):
		if b[i] == '1':
			tmp = 'x_%s' % (i)
			result += tmp
	return result


def generateEquaMonomes(mt, n):
	printColor("### Equations generation", MAGENTA)
	result = []
	for block in range(len(mt)):
		tmp = ''
		for bit in range(len(mt[block])):
			if mt[block][bit] == '1':
				if bit == 0:
					tmp += '1+' # constant
				else:
					tmp += bin2NsizeMonome(int2nsizeBin(bit, n), n) + '+'
		result.append(tmp.rstrip('+'))
	return result


def monomesNumber(equa, n):
	printColor("### Calculation of monomes number by degree", MAGENTA)
	tab = []
	for eq in range(len(equa)):
		result = [0 for i in range(n+1)]
		monomeList = equa[eq].split('+')
		for monome in monomeList:
			if monome == '1':
				result[0] += 1
			else:
				degree = len(monome.split('x_'))-1
				result[degree] += 1
		tab.append(result)
	print(tab)
	return tab


def distribution2BitsGraph(tab, n, display=False):
	data = np.asarray(tab)
	gap = np.ceil((np.max(data) - np.min(data)) / 8.).astype(int)
	fig = mpl.figure(figsize=(8, 6), dpi=100)
	ax = Axes3D(fig)
	xpos = np.arange(0,n,1)
	ypos = np.arange(0,n,1)
	xpos, ypos = np.meshgrid(xpos+0.25, ypos+0.25)
	xpos = xpos.flatten()
	ypos = ypos.flatten()
	zpos = np.zeros(n*n)
	dx = 0.5 * np.ones_like(zpos)
	dy = dx.copy()
	dz = data.flatten()
	for s in range(n**2):
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
	xyPos = [i+0.5 for i in range(n)]
	xyLab = [i for i in range(n)]
	mpl.xticks(xyPos, xyLab)
	mpl.yticks(xyPos, xyLab)
	if display:
		mpl.show()
	else:
		mpl.savefig('graph_2bit_bool_distrib.png', dpi=160)


def monomesGraph(tab, n, display=False):
	nvx = [i for i in range(n+1)]
	nvy = [n+0.5 for i in range(n+1)]
	nvz = [(0.5 * comb(n, i)) for i in range(n+1)]

	max = 0 # zscale definition
	for i in range(len(tab)):
		for j in range(len(tab[i])):
			if tab[i][j] > max:
				max = tab[i][j]

	xscale = [i for i in range(0, n+1, 1)] # degree of monome
	yscale = [i for i in range(n)] # bit number
	zscale = [i for i in range(0, max, int(max/n))] # number of monome

	fig = mpl.figure(figsize=(8, 6), dpi=100) # fig definition -> figsize=(16, 12)
	ax = fig.add_subplot(111, projection='3d')

	for i in range(n):
		ax.bar(xscale, tab[i], zs=i, zdir='y', align='center', color=rgb, alpha=1.0, edgecolor=rgbDark)
	ax.plot(nvx, nvy, zs=nvz, zdir='z', linewidth=4, color='r', marker='s', label='Loi normale', alpha=1.0)

	ax.set_xlabel('Degree of monomes')
	ax.set_xticks(xscale)
	ax.set_xticklabels(xscale, rotation=0, ha='center', va='center', size=8)

	ax.set_ylabel('Bit number')
	ax.set_yticks(yscale)
	ax.set_yticklabels(yscale, rotation=-90, ha='center', va='center', size=8)

	ax.set_zlabel('Monome number')
	ax.set_zticks(zscale)
	ax.set_zticklabels(zscale, rotation=0, ha='center', va='center', size=8)

	for item in ([ax.xaxis.label, ax.yaxis.label, ax.zaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()) + ax.get_zticklabels():
		item.set_fontsize(8)

	ax.legend(loc='lower left', prop={'size':8})
	ax.grid(True)
	for degree in [10, 230, 300, 350]:
		ax.view_init(4, degree)
		extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
		mpl.savefig('graph_'+str(degree)+'.png', dpi=160, bbox_inches=extent, pad_inches=0)
	if display:
		mpl.show()


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


def generateAleaBooleanFunction(n):
	"""Generate the Truth Table of a Boolean Function
	f(x): F_2^n to F_2^n -- Value of f(x) are random"""
	printColor("### Random Boolean functions generation", MAGENTA)
	result = []
	random.seed()
	for i in range(2**n):
		val = random.randint(0, (2**n)-1)
		result.append(int2nsizeBin(val, n))
	return result





if __name__ == "__main__":
	n = 16
	printColor("### Number of variables: %d" % n, MAGENTA)
	tt = generateAleaBooleanFunction(n)
	mt = generateMoebiusTransform(tt, n)
	equa = generateEquaMonomes(mt, n)
	tab = monomesNumber(equa, n)
	monomesGraph(tab, n, display=False)
	distrib = monomesDistribution(equa,n)
	distribution2BitsGraph(distrib, n, display=False)
