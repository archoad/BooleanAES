#! /usr/bin/env python
# -*- coding: utf-8 -*-


from libmain import *
from libsubbytes import *
from libshiftrows import *
from libmixcolumns import *
from libkeyexpansion import *




def writeSubBytes(numRound):
	printColor('## SubBytes %s' % numRound, GREEN)
	equa = subBytes()
	binMon = generateBinaryMonomes(equa)
	for i in xrange(blockSize):
		f = openFile(fileNameEnc+'%s.txt' % intToThreeChar(i))
		f.write('## subBytes%s\n' % numRound)
		f.write(binMon[i])
		closeFile(f)
	return equa


def writeShiftRows(numRound):
	printColor('## ShiftRows %s' % numRound, GREEN)
	equa = shiftRows()
	binMon = generateBinaryMonomes(equa)
	for i in xrange(blockSize):
		f = openFile(fileNameEnc+'%s.txt' % intToThreeChar(i))
		f.write('## shiftRows%s\n' % numRound)
		f.write(binMon[i])
		closeFile(f)
	return equa


def writeMixColumns(numRound):
	printColor('## MixColumns %s' % numRound, GREEN)
	equa = mixColumns()
	binMon = generateBinaryMonomes(equa)
	for i in xrange(blockSize):
		f = openFile(fileNameEnc+'%s.txt' % intToThreeChar(i))
		f.write('## mixColumns%s\n' % numRound)
		f.write(binMon[i])
		closeFile(f)
	return equa


def writeRound(numRound, equaSB, equaSR, equaMC):
	printColor('## Round %s' % numRound, GREEN)
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
		f = openFile(fileNameEnc+'%s.txt' % intToThreeChar(i))
		f.write('## Round%s\n' % numRound)
		f.write(binMon[i])
		closeFile(f)
	return resultMC


def treatAddRoundKey(value, key, clearBlock):
	result = ''
	for i in xrange(blockSize):
		if int(value[0].split('\t')[1][i]):
			result += xorTab(key[i], clearBlock[i])
		else:
			result += '0'
	return result


def treatBlock(value, block):
	"""Each monomial on the line is multiplied and each line is XORed"""
	result = []
	for polynom in value:
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


def controlBlock(start, end, block, key=None):
	flag = 0
	result = ''
	for i in xrange(blockSize):
		file = fileNameEnc+'%s.txt' % intToThreeChar(i)
		temp = extractBlock(file, start, end)
		if (key == None):
			result += treatBlock(temp, block)
		else:
			result += treatBlock(temp, key)

	if (key == None):
		block = result
	else:
		block = xorTab(result, block)
	printColor(start)
	print block, len(block)
	print bin2hex(block), len(bin2hex(block))
	return block


def generateStepsFiles():
	createAESFiles('enc')
	addRoundKey(0, 'enc')
	writeSubBytes(0)
	writeShiftRows(0)
	writeMixColumns(0)
	addRoundKey(1, 'enc')
	writeSubBytes(1)
	writeShiftRows(1)
	writeMixColumns(1)
	addRoundKey(2, 'enc')
	writeSubBytes(2)
	writeShiftRows(2)
	writeMixColumns(2)
	writeEndFlag('enc')
#	print currentStep, len(currentStep)
#	bitToLatex(currentStep[127])
	printColor('## Files generated', RED)


def controlStepsCipheringProcess():
	clearBlock = '00112233445566778899aabbccddeeff'
	key = '000102030405060708090a0b0c0d0e0f'
	fipsMixColumns2 = '4c9c1e66f771f0762c3f868e534df256'

	printColor('## Clear block %s' % (clearBlock), BLUE)
	print hexToBinBlock(clearBlock), len(hexToBinBlock(clearBlock))
	printColor('## Key block %s' % (key), BLUE)
	print hexToBinBlock(key), len(hexToBinBlock(key))

	key = hexToBinBlock(key)
	clearBlock = hexToBinBlock(clearBlock)

	block = controlBlock('## addRoundKey0', '## subBytes0', clearBlock, key)
	block = controlBlock('## subBytes0', '## shiftRows0', block)
	block = controlBlock('## shiftRows0', '## mixColumns0', block)
	block = controlBlock('## mixColumns0', '## addRoundKey1', block)
	block = controlBlock('## addRoundKey1', '## subBytes1', block, key)
	block = controlBlock('## subBytes1', '## shiftRows1', block)
	block = controlBlock('## shiftRows1', '## mixColumns1', block)
	block = controlBlock('## mixColumns1', '## addRoundKey2', block)
	block = controlBlock('## addRoundKey2', '## subBytes2', block, hexToBinBlock('d6aa74fdd2af72fadaa678f1d6ab76fe'))
	block = controlBlock('## subBytes2', '## shiftRows2', block)
	block = controlBlock('## shiftRows2', '## mixColumns2', block)
	block = controlBlock('## mixColumns2', '## end', block)
	print('%s (FIPS result)' % fipsMixColumns2)


def generateFullFiles():
	createAESFiles('enc')
	addRoundKey(0, 'enc')
	writeRound(0, subBytes(), shiftRows(), mixColumns())
	addRoundKey(1, 'enc')
	writeRound(1, subBytes(), shiftRows(), mixColumns())
	addRoundKey(2, 'enc')
	writeRound(2, subBytes(), shiftRows(), mixColumns())
	writeEndFlag('enc')
#	print currentStep, len(currentStep)
#	bitToLatex(currentStep[127])
	printColor('## Files generated', RED)


def controlFullCipheringProcess():
	clearBlock = '00112233445566778899aabbccddeeff'
	key = '000102030405060708090a0b0c0d0e0f'
	fipsMixColumns2 = '4c9c1e66f771f0762c3f868e534df256'

	printColor('## Clear block %s' % (clearBlock), BLUE)
	print hexToBinBlock(clearBlock), len(hexToBinBlock(clearBlock))
	printColor('## Key block %s' % (key), BLUE)
	print hexToBinBlock(key), len(hexToBinBlock(key))

	key = hexToBinBlock(key)
	clearBlock = hexToBinBlock(clearBlock)

	block = controlBlock('## addRoundKey0', '## Round0', clearBlock, key)
	block = controlBlock('## Round0', '## addRoundKey1', block)
	block = controlBlock('## addRoundKey1', '## Round1', block, key)
	block = controlBlock('## Round1', '## addRoundKey2', block)
	block = controlBlock('## addRoundKey2', '## Round2', block, hexToBinBlock('d6aa74fdd2af72fadaa678f1d6ab76fe'))
	block = controlBlock('## Round2', '## end', block)
	print('%s (FIPS result)' % (fipsMixColumns2))





if __name__ == "__main__":
#	testKeyExpansion()
	generateStepsFiles()
	controlStepsCipheringProcess()
	generateFullFiles()
	controlFullCipheringProcess()






