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


def treatLines(allLines, mode):
	result = []
	decalage = 0
	emptyLine = '0 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
	for line in allLines:
		line = line.rstrip('\n')
		if line.startswith('##'):
			result.append(line + '\n')
			decalage += 1
		else:
			line = line[:1] + ' ' + line[2:]
			line = ((decalage - 1) * (emptyLine + ' ')) + line + ((21 - decalage) * (' ' + emptyLine))
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
		print('bit number', i, ':', len(allLines), 'read lines,', len(result), 'treated lines')
	printColor('## Files generated', YELLOW)


def someTests():
	w = generateWord(4)
	print(w[0])
	print(equaToLatex(w[0]))
	print(len(w))

	equa = invSubBytes()
	print(equa[0])
	print(equaToLatex(equa[0]))
	print(len(equa))

	equa = invShiftRows()
	print(equa[0])
	print(equaToLatex(equa[0]))
	print(len(equa))

	equa = invMixColumns()
	print(equa[0])
	print(equaToLatex(equa[0]))
	print(len(equa))


if __name__ == "__main__":
	print(sys.version)
	someTests()
	#encryptionProcess(step=True, control=True)
	#decryptionProcess(step=True, control=True)
	#createFullFiles('enc')
	#createFullFiles('dec')
	#testKeyExpansion()
