#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os
from libminiaes import *


BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = xrange(30, 38)
directory = 'mini_AES_files/'




def printColor(string, color=RED):
	print '\033[1;%dm%s\033[0m' % (color, string)


def blockToStr(block):
	result = ''
	for i in xrange(blockSize):
		if ((i % nibbleSize) == 0) & (i <> 0): result += ' '
		result += block[i]
	return result


def xorTab(t1, t2):
	"""Takes two tabs t1 and t2 of same lengths and returns t1 XOR t2."""
	result = ''
	for i in xrange(len(t1)):
		result += str(int(t1[i]) ^ int(t2[i]))
	return result


def xorList(mylist):
	result = mylist[0]
	cpt = 0
	for i in xrange(len(mylist)):
		if cpt < len(mylist)-1:
			result = xorTab(result, mylist[cpt+1])
		cpt += 1
	return result


def intToThreeChar(i):
	"""Transform an integer to a 3 chars length string by adding 0
	uasge: intToThreeChar(12) return 012"""
	temp = str(i)
	result = ''
	if len(temp) == 1:
		result = '00' + temp
	elif len(temp) == 2:
		result = '0' + temp
	else:
		result = temp
	return result


def createFile(name):
	"""Create file named by "name" for data"""
	global directory
	f = open(directory+name, 'w')
	return f


def openFile(name):
	"""Open file named by "name" for data"""
	global directory
	f = open(directory+name, 'a')
	return f


def readFile(name):
	"""Read file called name and return a list in which one element corresponds to a line"""
	global directory
	f = open(directory+name, 'r')
	result = f.readlines()
	closeFile(f)
	return result


def closeFile(f):
	"""Close file handled by f"""
	if not(f.closed):
		f.close()
	return 0


def createMiniAESFiles():
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
	printColor('## Files generated', GREEN)
	return 1


def generateBitsBlock(c):
	"""Generate a string containing blockSize bits
	usage: generateGenericBlock('x3') return 000100...00000"""
	result = ''
	tmp = int(c.split('_')[1])
	for i in xrange(blockSize):
		if i == tmp:
			result += '1'
		else:
			result += '0'
	return result


def equaToLines(equa):
	result = ''
	tmp = equa.split('+')
	for monomial in tmp:
		if monomial == '1':
			result += '1\t'
			for i in xrange(1,blockSize+1):
				result += '0'
			result += '\n'
		else:
			result += '0\t'
			tmp = monomial.split('x')
			for i in xrange(1,blockSize+1):
				if str(i) in tmp:
					result += '1'
				else:
					result += '0'
			result += '\n'
	return(result)


def generateFiles():
	createMiniAESFiles()
	printColor('## Generating the truth table of function expansion key', GREEN)
	(k0, k1, k2) = generateRoundsKeysTruthTable()
	printColor('## Generating the truth table of function round one', GREEN)
	r1 = generateRoundOneTruthTable()
	printColor('## Generating the truth table of function round two', GREEN)
	r2 = generateRoundTwoTruthTable()
	printColor('## Calculating Moebius transform for K0', GREEN)
	mtk0 = generateMoebiusTransform(k0)
	printColor('## Calculating Moebius transform for K1', GREEN)
	mtk1 = generateMoebiusTransform(k1)
	printColor('## Calculating Moebius transform for K2', GREEN)
	mtk2 = generateMoebiusTransform(k2)
	printColor('## Calculating Moebius transform for R1', GREEN)
	mtr1 = generateMoebiusTransform(r1)
	printColor('## Calculating Moebius transform for R2', GREEN)
	mtr2 = generateMoebiusTransform(r2)
	for i in xrange(blockSize):
		printColor('## Generating file for bit %s' % (i+1), MAGENTA)
		f = openFile('f_%s.txt' % (intToThreeChar(i)))

		equa = definesMonomeBlock(mtk0[i])
		f.write('## addRoundKey1\n')
		f.write('%s' % (equaToLines(equa)))

		equa = definesMonomeBlock(mtr1[i])
		f.write('## RoundOne\n')
		f.write('%s' % (equaToLines(equa)))

		equa = definesMonomeBlock(mtk1[i])
		f.write('## addRoundKey2\n')
		f.write('%s' % (equaToLines(equa)))

		equa = definesMonomeBlock(mtr2[i])
		f.write('## RoundTwo\n')
		f.write('%s' % (equaToLines(equa)))

		equa = definesMonomeBlock(mtk2[i])
		f.write('## addRoundKey3\n')
		f.write('%s' % (equaToLines(equa)))

		f.write('## end\n')
		closeFile(f)


def treatBlock(roundBlock, block):
	"""Each monomial on the line is multiplied and each line is XORed"""
	result = []
	for polynom in roundBlock:
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


def treatKey(beginMark, endMark, key, clear):
	result = ''
	for i in xrange(blockSize):
		temp = []
		flag = 0
		allLines = readFile('f_%s.txt' % (intToThreeChar(i)))
		for line in allLines:
			line = line.rstrip('\n')
			if line == beginMark: flag = 1
			if line == endMark: flag = 0
			if flag:
				if line[0] <> '#':
					temp.append(line)
		result += treatBlock(temp, key)
	return(xorTab(clear, result))


def treatRound(beginMark, endMark, block):
	result = ''
	for i in xrange(blockSize):
		temp = []
		flag = 0
		allLines = readFile('f_%s.txt' % (intToThreeChar(i)))
		for line in allLines:
			line = line.rstrip('\n')
			if line == beginMark: flag = 1
			if line == endMark: flag = 0
			if flag:
				if line[0] <> '#':
					temp.append(line)
		result += treatBlock(temp, block)
	return(result)


def controlCipheringProcess():
	clear = '1001110001100011'
	key = '1100001111110000'
	printColor('## Clear block %s' % blockToStr(clear), BLUE)
	printColor('## Key block %s' % blockToStr(key), BLUE)

	block = treatKey('## addRoundKey1', '## RoundOne', key, clear)
	printColor('## addRoundKey')
	print blockToStr(block)

	block = treatRound('## RoundOne', '## addRoundKey2', block)
	printColor('## RoundOne')
	print blockToStr(block)

	block = treatKey('## addRoundKey2', '## RoundTwo', key, block)
	printColor('## addRoundKey')
	print blockToStr(block)

	block = treatRound('## RoundTwo', '## addRoundKey3', block)
	printColor('## RoundTwo')
	print blockToStr(block)

	block = treatKey('## addRoundKey3', '## end', key, block)
	printColor('## addRoundKey')
	print blockToStr(block)

	printColor('## Cipher block %s' % blockToStr(block), BLUE)






if __name__ == "__main__":
#	generateFiles()
	controlCipheringProcess()
