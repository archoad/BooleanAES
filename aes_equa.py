#! /usr/bin/env python
# -*- coding: utf-8 -*-


from libmain import *
from libsubbytes import *
from libmixcolumns import *
from libkeyexpansion import *




def writeEndFlag():
	for i in xrange(blockSize):
		f = openFile('f_%s.txt' % (intToThreeChar(i)))
		f.write('## end\n')
		closeFile(f)


def addRoundKey(numRound):
	printColor('## AddRoundKey %s' % numRound, GREEN)
	result = []
	if numRound == 0:
		result = generateKn(generateW0(), generateW1(), generateW2(), generateW3())
		clearBlock = generateGenericBlock('x')
		for i in xrange(blockSize):
			f = openFile('f_%s.txt' % (intToThreeChar(i)))
			f.write('## addRoundKey0\n')
			f.write('0\t%s\n0\t%s\n' % (generateBitsBlock(clearBlock[i]), generateBitsBlock(result[i])))
			closeFile(f)
	else:
		if numRound == 1:
			result = generateKn(generateW4(), generateW5(), generateW6(), generateW7())
		elif numRound == 2:
			result = generateKn(generateW8(), generateW9(), generateW10(), generateW11())
		binMon = generateBinaryMonomes(result)
		for i in xrange(blockSize):
			f = openFile('f_%s.txt' % (intToThreeChar(i)))
			f.write('## addRoundKey%s\n' % numRound)
			f.write(binMon[i])
			closeFile(f)
	return result


def subBytes(numRound):
	printColor('## SubBytes %s' % numRound, GREEN)
	tt = generateSboxTruthTable()
	mt = generateMoebiusTransform(tt)
	equations = generateEquaMonomes(mt)
	equaAES = generateEquaMonomesAES(equations)
	binMon = generateBinaryMonomes(equaAES)
	for i in xrange(blockSize):
		f = openFile('f_%s.txt' % (intToThreeChar(i)))
		f.write('## subBytes%s\n' % numRound)
		f.write(binMon[i])
		closeFile(f)
	return equaAES


def shiftRows(numRound):
	printColor('## ShiftRows %s' % numRound, GREEN)
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
		f = openFile('f_%s.txt' % (intToThreeChar(i)))
		f.write('## shiftRows%s\n' % numRound)
		f.write('0\t' + SR[i] + '\n')
		closeFile(f)
	for i in xrange(blockSize):
		for bit in xrange(blockSize):
			if SR[i][bit] == '1':
				equa.append('x_%s' % (bit))
	return equa


def mixColumns(numRound):
	printColor('## MixColumns %s' % numRound, GREEN)
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
		f = openFile('f_%s.txt' % (intToThreeChar(i)))
		f.write('## mixColumns%s\n' % numRound)
		f.write(result[i])
		closeFile(f)

	for i in xrange(blockSize):
		tmp = result[i].split('\n')
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


def controlARK0(key, clearBlock):
	result = []
	flag = 0
	for i in xrange(blockSize):
		allLines = readFile('f_%s.txt' % (intToThreeChar(i)))
		temp = []
		for line in allLines:
			line = line.rstrip('\n')
			if line == '## addRoundKey0': flag = 1
			if line == '## subBytes0': flag = 0
			if flag:
				if line[0] <> '#':
					temp.append(line)
		result.append(treatAddRoundKey(temp, key, clearBlock))
	block = xorList(result)
	printColor('## addRoundKey0')
	print block, len(block)
	print bin2hex(block), len(bin2hex(block))
	return block


def controlBlock(start, end, block, key=None):
	flag = 0
	result = ''
	for i in xrange(blockSize):
		allLines = readFile('f_%s.txt' % (intToThreeChar(i)))
		temp = []
		for line in allLines:
			line = line.rstrip('\n')
			if line == start: flag = 1
			if line == end: flag = 0
			if flag:
				if line[0] <> '#':
					temp.append(line)
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


def generateFiles():
	createAESFiles()

	step1 = addRoundKey(0)
#	print step1, len(step1)
#	bitToLatex(step1[127])
	step2 = subBytes(0)
	step3 = shiftRows(0)
	step4 = mixColumns(0)
	step5 = addRoundKey(1)
	step6 = subBytes(1)
	step7 = shiftRows(1)
	step8 = mixColumns(1)
	step9 = addRoundKey(2)
	step10 = subBytes(2)
	step11 = shiftRows(2)
	step12 = mixColumns(2)

	writeEndFlag()
	printColor('## Files generated', RED)


def controlCipheringProcess():
	clearBlock = '3243f6a8885a308d313198a2e0370734'
	key = '2b7e151628aed2a6abf7158809cf4f3c'
	fipsAddRoundKey0 = '193de3bea0f4e22b9ac68d2ae9f84808'
	fipsMixColumn0 = '046681e5e0cb199a48f8d37a2806264c'
	fipsAddRoundKey1 = 'a49c7ff2689f352b6b5bea43026a5049'
	fipsMixColumn1 = '584dcaf11b4b5aacdbe7caa81b6bb0e5'
	fipsAddRoundKey2 = 'aa8f5f0361dde3ef82d24ad26832469a'

#	clearBlock = '00112233445566778899aabbccddeeff'
#	key = '000102030405060708090a0b0c0d0e0f'
#	fipsAddRoundKey0 = '00102030405060708090a0b0c0d0e0f0'
#	fipsMixColumn0 = '5f72641557f5bc92f7be3b291db9f91a'
#	fipsAddRoundKey1 = '89d810e8855ace682d1843d8cb128fe4'
#	fipsMixColumn1 = 'ff87968431d86a51645151fa773ad009'
#	fipsAddRoundKey2 = '4915598f55e5d7a0daca94fa1f0a63f7'

	printColor('## Clear block %s' % (clearBlock), BLUE)
	printColor('## Key block %s' % (key), BLUE)
	key = hexToBinBlock(key)
	clearBlock = hexToBinBlock(clearBlock)

	block = controlARK0(key, clearBlock)
	print('%s (FIPS result)' % (fipsAddRoundKey0))

	block = controlBlock('## subBytes0', '## shiftRows0', block)
	block = controlBlock('## shiftRows0', '## mixColumns0', block)
	block = controlBlock('## mixColumns0', '## addRoundKey1', block)
	print('%s (FIPS result)' % (fipsMixColumn0))
	block = controlBlock('## addRoundKey1', '## subBytes1', block, key)
	print('%s (FIPS result)' % (fipsAddRoundKey1))
	block = controlBlock('## subBytes1', '## shiftRows1', block)
	block = controlBlock('## shiftRows1', '## mixColumns1', block)
	block = controlBlock('## mixColumns1', '## addRoundKey2', block)
	print('%s (FIPS result)' % (fipsMixColumn1))
	block = controlBlock('## addRoundKey2', '## subBytes2', block, hexToBinBlock('a0fafe1788542cb123a339392a6c7605'))
#	block = controlBlock('## addRoundKey2', '## subBytes2', block, hexToBinBlock('d6aa74fdd2af72fadaa678f1d6ab76fe'))
	print('%s (FIPS result)' % (fipsAddRoundKey2))
	block = controlBlock('## subBytes2', '## shiftRows2', block)
	block = controlBlock('## shiftRows2', '## mixColumns2', block)
	block = controlBlock('## mixColumns2', '## end', block)



def testKeyExpansion():
	w4 = generateW4()
	testWord(w4, '2b7e151628aed2a6abf7158809cf4f3c') # R0 key (w0, w1, w2, w3)
	w8 = generateW8()
	testWord(w8, 'a0fafe1788542cb123a339392a6c7605') # R1 key (w4, w5, w6, w7)
	w12 = generateW12()
	testWord(w12, 'f2c295f27a96b9435935807a7359f67f') # R2 key (w8, w9, w10, w11)




if __name__ == "__main__":
	testKeyExpansion()
#	generateFiles()
#	controlCipheringProcess()






