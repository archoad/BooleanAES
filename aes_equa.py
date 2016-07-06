#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from libmain import *
from libsubbytes import *
from libshiftrows import *
from libmixcolumns import *
from libkeyexpansion import *
from libequaenc import *
from libequadec import *




def encryptionProcess(step=False, control=False):
	if step:
		generateEncStepsFiles()
		if control:
			controlEncStepsFiles()
	else:
		generateEncFullFiles()
		if control:
			controlEncFullFiles()


def decryptionProcess(step=False, control=False):
	if step:
		generateDecStepsFiles()
		if control:
			controlDecStepsFiles()
	else:
		generateDecFullFiles()
		if control:
			controlDecFullFiles()


def getNumRound(line):
	line = line[3:len(line)]
	if line.startswith('add'):
		n = line[11:len(line)]
	if line.startswith('Round'):
		n = line[5:len(line)]
	if line.startswith('invM'):
		n = line[13:len(line)]
	if line.startswith('end'):
		n = 100
	return int(n)


def treatLines(allLines, mode):
	result = []
	emptyLine = '0 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
	for line in allLines:
		line = line.rstrip('\n')
		if line.startswith('##'):
			numRound = getNumRound(line)
			result.append(line + '\n')
		else:
			line = line[:1] + ' ' + line[2:]
			line = (numRound * (emptyLine + ' ')) + line + ((10 - numRound) * (' ' + emptyLine))
			result.append(line + '\n')
	return result


def createFullFiles(mode):
	testAESdirectory()
	(generateEncFullFiles() if mode == 'enc' else generateDecFullFiles())
	for i in range(blockSize):
		fname = (fileNameEnc if mode == 'enc' else fileNameDec)
		fileName = fname+'%s.txt' % intToThreeChar(i)
		allLines = readFile(fileName)
		result = treatLines(allLines, mode)
		f = open(directory+fileName, 'w')
		for line in result:
			f.write(line)
		closeFile(f)
		print('bit number', i, ':', len(allLines), 'lines readed,', len(result), 'lines treated')
	printColor('## Files generated', YELLOW)


def someTests():
	w = generateWord(4)
	print(w[0])
	print(equaToLatex(w[0]))
	print(len(w))
	r = generateRoundEnc(subBytes(), shiftRows(), mixColumns())
	print(r[0])
	print(equaToLatex(r[0]))
	print(len(r))
	equa = invSubBytes()
	print(equa[0])
	print(len(equa))
	print(equaToLatex(equa[0]))
	equa = invShiftRows()
	print(equa[0])
	print(len(equa))
	print(equaToLatex(equa[0]))
	equa = invMixColumns()
	print(equa[0])
	print(len(equa))
	print(equaToLatex(equa[0]))


if __name__ == "__main__":
	print(sys.version)
	someTests()
	#encryptionProcess(step=True, control=True)
	#decryptionProcess(step=True, control=True)
	#createFullFiles('enc')
	#createFullFiles('dec')
	#testKeyExpansion()
