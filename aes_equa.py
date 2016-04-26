#! /usr/bin/env python
# -*- coding: utf-8 -*-

import shutil

from libmain import *
from libsubbytes import *
from libshiftrows import *
from libmixcolumns import *
from libkeyexpansion import *
from libkeyexpansion import *
from libequaenc import *
from libequadec import *


def testAESdirectory():
	d = os.path.dirname(directory)
	if os.path.exists(d):
		printColor('## Deleting directory %s' % (d), RED)
		shutil.rmtree(directory)


def encryptionProcess(step=True):
	if (step):
		generateEncStepsFiles()
		controlEncStepsFiles()
	else:
		generateEncFullFiles()
		controlEncFullFiles()


def decryptionProcess(step=True):
	if (step):
		generateDecStepsFiles()
		controlDecStepsFiles()
	else:
		generateDecFullFiles()
		controlDecFullFiles()


def getNumRoundEnc(line):
	line = line[3:len(line)]
	if line.startswith('add'):
		n = line[11:len(line)]
	if line.startswith('Round'):
		n = line[5:len(line)]
	if line.startswith('end'):
		n = 100
	return int(n)


def treatLines(allLines):
	result = []
	emptyLine = '0 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
	for line in allLines:
		line = line.rstrip('\n')
		if line.startswith('##'):
			numRound = getNumRoundEnc(line)
			result.append(line + '\n')
		else:
			line = line[:1] + ' ' + line[2:]
			line = (numRound * (emptyLine + ' ')) + line + ((10 - numRound) * (' ' + emptyLine))
			result.append(line + '\n')
	return result


def createFullEncryptionFiles():
	testAESdirectory()
	generateEncFullFiles()
	for i in xrange(blockSize):
		fileName = fileNameEnc+'%s.txt' % intToThreeChar(i)
		allLines = readFile(fileName)
		result = treatLines(allLines)
		f = open(directory+fileName, 'w')
		for line in result:
			f.write(line)
		closeFile(f)
		print 'bit number', i, ':', len(allLines), 'lines readed,', len(result), 'lines treated'
	printColor('## Files generated', RED)




if __name__ == "__main__":
	#testKeyExpansion()
	#encryptionProcess()
	#decryptionProcess()
	createFullEncryptionFiles()
