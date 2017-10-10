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


def createFullFiles(mode, createDir=True):
	if createDir:
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
	#equa = subBytes()
	#equa = shiftRows()
	#equa = mixColumns()
	#equa = invSubBytes()
	#equa = invShiftRows()
	#equa = invMixColumns()
	#equa = generateWord(4)
	#print(equa[0], len(equa), end='\n\n')
	#print(equaToLatex(equa[0], 'k'), end='\n\n')
	#print(len(equa), end='\n\n')
	#for bit in range(120, 128, 1):
	#	val = equaToLatex(equa[bit], 'b').strip('$')
	#	print('\\text{MixColumns}(b_{%s}) = %s \\\\' % (bit, val))
	# génération de l'équation pour un tour
	equa = generateRoundEncEqua(subBytes(), shiftRows(), mixColumns())
	equa = reduceEqua(equa)
	#equa = generateRoundDecEqua(invSubBytes(), invShiftRows())
	#equaKey = generateWord(4)
	#print("$b'_0 = %s \\oplus %s$" % (equaToLatex(equa[0], 'b').strip('$'), equaToLatex(equaKey[0], 'k').strip('$')))




if __name__ == "__main__":
	print(sys.version)
	#someTests()
	encryptionProcess(step=False, control=True)
	#decryptionProcess(step=False, control=True)
	#createFullFiles('enc', createDir=True)
	#createFullFiles('dec', createDir=False)
	#testKeyExpansion()
