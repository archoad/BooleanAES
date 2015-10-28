#! /usr/bin/env python
# -*- coding: utf-8 -*-


from libmain import *
from libsubbytes import *
from libshiftrows import *
from libmixcolumns import *
from libkeyexpansion import *




def writeInvSubBytes(numRound):
	printColor('## InvSubBytes %s' % numRound, GREEN)
	equa = invSubBytes()
	binMon = generateBinaryMonomes(equa)
	for i in xrange(blockSize):
		f = openFile(fileNameDec+'%s.txt' % intToThreeChar(i))
		f.write('## invSubBytes%s\n' % numRound)
		f.write(binMon[i])
		closeFile(f)
	return equa


def writeInvShiftRows(numRound):
	printColor('## InvShiftRows %s' % numRound, GREEN)
	equa = invShiftRows()
	binMon = generateBinaryMonomes(equa)
	for i in xrange(blockSize):
		f = openFile(fileNameDec+'%s.txt' % intToThreeChar(i))
		f.write('## invShiftRows%s\n' % numRound)
		f.write(binMon[i])
		closeFile(f)
	return equa


def writeInvMixColumns(numRound):
	printColor('## InvMixColumns %s' % numRound, GREEN)
	equa = invMixColumns()
	binMon = generateBinaryMonomes(equa)
	for i in xrange(blockSize):
		f = openFile(fileNameDec+'%s.txt' % intToThreeChar(i))
		f.write('## invMixColumns%s\n' % numRound)
		f.write(binMon[i])
		closeFile(f)
	return equa


def writeRound(numRound, equaSB, equaSR):
	printColor('## Round %s' % numRound, GREEN)
	resultSR = []
	for i in xrange(blockSize):
		equaSR[i] = equaSR[i].split('_')
		resultSR.append(equaSB[int(equaSR[i][1])])
	binMon = generateBinaryMonomes(resultSR)

	for i in xrange(blockSize):
		f = openFile(fileNameDec+'%s.txt' % intToThreeChar(i))
		f.write('## Round%s\n' % numRound)
		f.write(binMon[i])
		closeFile(f)
	return resultSR


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
		file = fileNameDec+'%s.txt' % intToThreeChar(i)
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
	createAESFiles('dec')
	writeInvShiftRows(2)
	writeInvSubBytes(2)
	addRoundKey(2, 'dec')
	writeInvMixColumns(2)
	writeInvShiftRows(1)
	writeInvSubBytes(1)
	addRoundKey(1, 'dec')
	writeInvMixColumns(1)
	writeInvShiftRows(0)
	writeInvSubBytes(0)
	addRoundKey(0, 'dec')
	writeEndFlag('dec')
#	print currentStep, len(currentStep)
#	bitToLatex(currentStep[127])
	printColor('## Files generated', RED)


def controlStepsDecipheringProcess():
	cipherBlock = '3bd92268fc74fb735767cbe0c0590e2d'
	key = '000102030405060708090a0b0c0d0e0f'
	clearBlock = '00112233445566778899aabbccddeeff'

	printColor('## Cipher block %s' % (cipherBlock), BLUE)
	print hexToBinBlock(cipherBlock), len(hexToBinBlock(cipherBlock))
	printColor('## Key block %s' % (key), BLUE)
	print hexToBinBlock(key), len(hexToBinBlock(key))

	key = hexToBinBlock(key)
	cipherBlock = hexToBinBlock(cipherBlock)

	block = controlBlock('## invShiftRows2', '## invSubBytes2', cipherBlock)
	block = controlBlock('## invSubBytes2', '## addRoundKey2', block)
	block = controlBlock('## addRoundKey2', '## invMixColumns2', block, hex2bin('d6aa74fdd2af72fadaa678f1d6ab76fe'))
	block = controlBlock('## invMixColumns2', '## invShiftRows1', block)
	block = controlBlock('## invShiftRows1', '## invSubBytes1', block)
	block = controlBlock('## invSubBytes1', '## addRoundKey1', block)
	block = controlBlock('## addRoundKey1', '## invMixColumns1', block, key)
	block = controlBlock('## invMixColumns1', '## invShiftRows0', block)
	block = controlBlock('## invShiftRows0', '## invSubBytes0', block)
	block = controlBlock('## invSubBytes0', '## addRoundKey0', block)
	block = controlBlock('## addRoundKey0', '## end', block, key)
	print('%s (FIPS result)' % clearBlock)
	return block


def generateFullFiles():
	createAESFiles('dec')
	writeRound(2, invSubBytes(), invShiftRows())
	addRoundKey(2, 'dec')
	writeInvMixColumns(2)
	writeRound(1, invSubBytes(), invShiftRows())
	addRoundKey(1, 'dec')
	writeInvMixColumns(1)
	writeRound(0, invSubBytes(), invShiftRows())
	addRoundKey(0, 'dec')
#	print currentStep, len(currentStep)
#	bitToLatex(currentStep[127])
	writeEndFlag('dec')
	printColor('## Files generated', RED)


def controlFullCipheringProcess():
	cipherBlock = '3bd92268fc74fb735767cbe0c0590e2d'
	key = '000102030405060708090a0b0c0d0e0f'
	clearBlock = '00112233445566778899aabbccddeeff'

	printColor('## Cipher block %s' % (cipherBlock), BLUE)
	print hexToBinBlock(cipherBlock), len(hexToBinBlock(cipherBlock))
	printColor('## Key block %s' % (key), BLUE)
	print hexToBinBlock(key), len(hexToBinBlock(key))

	key = hexToBinBlock(key)
	cipherBlock = hexToBinBlock(cipherBlock)

	block = controlBlock('## Round2', '## addRoundKey2', cipherBlock)
	block = controlBlock('## addRoundKey2', '## invMixColumns2', block, hex2bin('d6aa74fdd2af72fadaa678f1d6ab76fe'))
	block = controlBlock('## invMixColumns2', '## Round1', block)
	block = controlBlock('## Round1', '## addRoundKey1', block)
	block = controlBlock('## addRoundKey1', '## invMixColumns1', block, key)
	block = controlBlock('## invMixColumns1', '## Round0', block)
	block = controlBlock('## Round0', '## addRoundKey0', block)
	block = controlBlock('## addRoundKey0', '## end', block, key)
	print('%s (FIPS result)' % clearBlock)


if __name__ == "__main__":
	generateStepsFiles()
	controlStepsDecipheringProcess()
	generateFullFiles()
	controlFullCipheringProcess()






