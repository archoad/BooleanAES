#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os
from libmain import *
from libsubbytes import *
from libmixcolumns import *


def createAESFiles():
	global directory
	d = os.path.dirname(directory)
	if not os.path.exists(d):
		printColor('## Create directory %s' % (d), GREEN)
		os.mkdir(directory)
	else:
		printColor('## Directory %s already exist' % (d), RED)
	for i in xrange(blockSize):
		f = createFile('f_%s.txt' % (intToThreeChar(i)))
		closeFile(f)
	return 1


def generateGenericBlock(c):
	"""Generate a tab containing blockSize variables
	usage: generateGenericBlock('x') return ['x_0', 'x_1', 'x_2', 'x_3', 'x_4', ..., 'x_126', 'x_127']"""
	result = []
	for i in xrange(blockSize):
		result.append('%s_%s' % (c, i))
	return result


def generateBitsBlock(c):
	"""Generate a string containing blockSize bits
	usage: generateGenericBlock('x_3') return 00010000000...00000"""
	result = ''
	tmp = int(c.split('_')[1])
	for i in xrange(blockSize):
		if i == tmp:
			result += '1'
		else:
			result += '0'
	return result


def generateAllBits():
	"""Generate a list containing 128 input corresponding to the
		conversion of integer to binary for i in xrange(blockSize)"""
	result = []
	tmp = []
	for i in xrange(blockSize):
		tmp.append('0')
	for i in xrange(blockSize):
		t = ''
		tmp[i] = '1'
		result.append('0\t' + t.join(tmp) + '\r\n')
		tmp[i] = '0'
	return result


def addRoundKey(block, keyBlock):
	printColor('## AddRoundKey', GREEN)
	result = []
	for i in xrange(blockSize):
		result.append('%s+%s' % (block[i], keyBlock[i]))
		f = openFile('f_%s.txt' % (intToThreeChar(i)))
		f.write('## addRoundKey\r\n')
		f.write('0\t%s\r\n0\t%s\r\n' % (generateBitsBlock(block[i]), generateBitsBlock(keyBlock[i])))
		closeFile(f)
	return result


def subBytes():
	tt = generateSboxTruthTable()
	rm = generateMoebiusTransform(tt)
	equations = generateEquaMonomes(rm)
	equa = generateEquaMonomesAES(equations)
	return equa


def shiftRows():
	Nb = 4
	result = []
	SR = []
	equa = []
	state = [[(i*Nb)+j for i in xrange(Nb)] for j in xrange(Nb)]
	tmp = [[0 for i in xrange(Nb)] for i in xrange(Nb)]
	for i in xrange(Nb):
		for j in xrange(Nb):
			tmp[i][j] = state[i][(j + i) % Nb]
	for row in xrange(Nb):
		for byte in xrange(Nb):
			result.append(tmp[byte][row])
	for numByte in result:
		for i in xrange(octetSize):
			SR.append(generateBitsBlock('x_' + str((numByte*octetSize)+i)))
	for i in xrange(blockSize):
		for bit in xrange(blockSize):
			if SR[i][bit] == '1':
				equa.append('x_%s' % (bit))
	return equa


def mixColumns():
	equa = []
	result = ['' for i in xrange(blockSize)]
	tt2 = generateMultBy02TruthTable()
	tt3 = generateMultBy03TruthTable()
	mt2 = generateMoebiusTransform(tt2)
	mt3 = generateMoebiusTransform(tt3)
	equations2 = generateEquaMonomes(mt2)
	equations3 = generateEquaMonomes(mt3)
	equaAES2 = generateEquaMonomesAES(equations2)
	equaAES3 = generateEquaMonomesAES(equations3)
	binMon2 = generateBinaryMonomes(equaAES2)
	binMon3 = generateBinaryMonomes(equaAES3)
	bits = generateAllBits()

	for cpt in xrange(4):
		for i in xrange(octetSize):
			val = i + (cpt*32)
			result[val] = binMon2[val] + binMon3[val+8] + bits[val+16] + bits[val+24]
			result[val+8] = bits[val] + binMon2[val+8] + binMon3[val+16] + bits[val+24]
			result[val+16] = bits[val] + bits[val+8] + binMon2[val+16] + binMon3[val+24]
			result[val+24] = binMon3[val] + bits[val+8] + bits[val+16] + binMon2[val+24]

	for i in xrange(blockSize):
		tmp = result[i].split('\r\n')
		tmp.pop()
		eq = ''
		for monome in tmp:
			t = monome.split('\t')
			if t[0] == '1':
				eq += '1+'
			for bit in xrange(blockSize):
				if t[1][bit] == '1':
					eq += 'x_%s' % (bit)
			eq += '+'
		equa.append(eq.rstrip('+'))
	return equa


def equaRound(equaSB, equaSR, equaMC):
	printColor('## Round', GREEN)
	resultSR = []
	resultMC = []
	for i in xrange(blockSize):
		equaSR[i] = equaSR[i].split('_')
		resultSR.append(equaSB[int(equaSR[i][1])])

	for i in xrange(blockSize):
		tmp = ''
		for monomial in equaMC[i].split('+'):
			tmp += resultSR[int(monomial.split('_')[1])]
			tmp += '+'
		resultMC.append(tmp.rstrip('+'))
	binMon = generateBinaryMonomes(resultMC)

	for i in xrange(blockSize):
		f = openFile('f_%s.txt' % (intToThreeChar(i)))
		f.write('## Round\r\n')
		f.write(binMon[i])
		f.write('## end\r\n')
		closeFile(f)
	return resultMC


def treatAddRoundKey(ARK, key, clearBlock):
	result = ''
	for i in xrange(blockSize):
		if int(ARK[0].split('\t')[1][i]):
			result += xorTab(key[i], clearBlock[i])
		else:
			result += '0'
	return result


def treatSB_MC_SR(SB_MC_SR, block):
	"""Each monomial on the line is multiplied and each line is XORed"""
	result = []
	for polynom in SB_MC_SR:
		t = []
		tmp = polynom.split('\t')
		if tmp[0] == '1':
			result.append(int(tmp[0]))
		else:
			for i in xrange(blockSize):
				if tmp[1][i] == '1':
					t.append(int(block[i]))
			result.append(reduce(lambda x, y: x&y, t))
	return str(reduce(lambda x, y: x^y, result))


def generateFiles():
	createAESFiles()
	clearBlock = generateGenericBlock('x')
	keyBlock = generateGenericBlock('k')
#	print clearBlock, len(clearBlock)
#	print keyBlock, len(keyBlock)

	equaSB = subBytes()
	equaSR = shiftRows()
	equaMC = mixColumns()

	step1 = addRoundKey(clearBlock, keyBlock)
#	print step1, len(step1)
#	bitToLatex(step1[127])

	step2 = equaRound(equaSB, equaSR, equaMC)
#	print step2, len(step2)
#	bitToLatex(step2[127])

	printColor('## Files generated', RED)


def controlCipheringProcess():
	clearBlock = '3243f6a8885a308d313198a2e0370734'
	key = '2b7e151628aed2a6abf7158809cf4f3c'
	printColor('## Clear block %s' % (clearBlock), BLUE)
	printColor('## Key block %s' % (key), BLUE)
	key = hexToBinBlock(key)
	clearBlock = hexToBinBlock(clearBlock)
	result = []
	for i in xrange(blockSize):
		allLines = readFile('f_%s.txt' % (intToThreeChar(i)))
		temp = []
		for line in allLines:
			line = line.rstrip('\r\n')
			if line == '## addRoundKey': flag = 1
			if line == '## Round': flag = 0
			if flag:
				if line[0] <> '#':
					temp.append(line)
		result.append(treatAddRoundKey(temp, key, clearBlock))
	block = xorList(result)
	printColor('## addRoundKey')
	print block, len(block)
	print bin2hex(block), len(bin2hex(block))
	result = ''
	for i in xrange(blockSize):
		allLines = readFile('f_%s.txt' % (intToThreeChar(i)))
		temp = []
		for line in allLines:
			line = line.rstrip('\r\n')
			if line == '## Round': flag = 1
			if line == '## end': flag = 0
			if flag:
				if line[0] <> '#':
					temp.append(line)
		result += treatSB_MC_SR(temp, block)
	block = result
	printColor('## subBytes and shiftRows')
	print block, len(block)
	print bin2hex(block), len(bin2hex(block))


if __name__ == "__main__":
	generateFiles()
	controlCipheringProcess()



