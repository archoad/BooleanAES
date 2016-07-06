#! /usr/bin/env python
# -*- coding: utf-8 -*-

import random
from mpl_toolkits.mplot3d import Axes3D
from scipy.misc import comb
import matplotlib.pyplot as mpl
import numpy as np

from libminiaes import *



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


def generateEquaMonomes(mt):
	equa = []
	for i in range(blockSize):
		eq = definesMonomeBlock(mt[i])
		equa.append(eq)
	return equa


def monomesNumber(equa):
	tab = []
	for i in range(blockSize):
		eq = equa[i]
		print('Bit number %s --> ' % (i), eq,)
		result = [0 for i in range(blockSize)]
		monomeList = eq.split('+')
		for monome in monomeList:
			if monome == '1':
				result[0] += 1
			else:
				degree = len(monome.split('x'))-1
				result[degree] += 1
		print(result,)
		print
		tab.append(result)
	return tab


def monomesGraph(tab, text, display=False):
	max = 0 # zscale definition
	for i in range(blockSize):
		for j in range(len(tab[i])):
			if tab[i][j] > max:
				max = tab[i][j]
	xscale = [i for i in range(blockSize)] # degree of monome
	yscale = [i for i in range(blockSize)] # bit number
	zscale = [i for i in range(0, max, 2)] # number of monome

	fig = mpl.figure(figsize=(8, 6), dpi=100) # fig definition -> figsize=(16, 12)
	ax = fig.add_subplot(111, projection='3d')

	for i in range(blockSize):
		ax.bar(xscale, tab[i], zs=i, zdir='y', align='center', color=rgb, alpha=1.0, edgecolor=rgbDark)

	ax.set_xlabel('Degree of monome')
	ax.set_xticks(xscale)
	ax.set_xticklabels(xscale, rotation=0, ha='center', va='center', size=8)

	ax.set_ylabel('Bit number')
	ax.set_yticks(yscale)
	ax.set_yticklabels(yscale, rotation=-90, ha='center', va='center', size=8)

	ax.set_zlabel('Monome number')
	ax.set_zticks(zscale)
	ax.set_zticklabels(zscale, rotation=0, ha='center', va='center', size=8)

	ax.grid(True)
	for degree in [230, 300]:
		ax.view_init(4, degree)
		extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
		mpl.savefig('graph_'+str(degree)+'_'+text+'.png', dpi=160, bbox_inches=extent, pad_inches=0)
	if display:
		mpl.show()


def monomesDistribution(equa):
	numMonom = [[0 for i in range(blockSize)] for i in range(blockSize)]
	for num in range(blockSize):
		tmp = equa[num].split('+')
		for mon in tmp:
			monom = mon.split('x')
			del monom[0]
			l = len(monom)
			if l >1:
				for r in range(0, l-1, 1):
					numMonom[int(monom[r])-1][int(monom[r+1])-1] += 1
	for item in numMonom:
		print(item)
	return numMonom


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
	zpos = np.zeros(blockSize**2)
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
	xyPos = [i+0.5 for i in range(blockSize)]
	xyLab = [i for i in range(blockSize)]
	mpl.xticks(xyPos, xyLab)
	mpl.yticks(xyPos, xyLab)
	if display:
		mpl.show()
	else:
		mpl.savefig('graph_2bit_'+name+'_distrib.png', dpi=160)




if __name__ == "__main__":
	(k0, k1, k2) = generateRoundsKeysTruthTable()
#	r1 = generateRoundOneTruthTable()
#	r2 = generateRoundTwoTruthTable()
#	tt = generateNibbleSubTruthTable()
#	tt = generateShiftRowTruthTable()
#	tt = generateMixColumnsTruthTable()

	mt = generateMoebiusTransform(k2)
	equa = generateEquaMonomes(mt)
	tab = monomesNumber(equa)
	monomesGraph(tab, 'k2', display=False)
	distrib = monomesDistribution(equa)
	distribution2BitsGraph(distrib, 'k2', display=False)
