

from libmain import *


def generateMultByValTruthTable(val):
	result = []
	multiplier = hex2bin(val)
	for i in range(2**octetSize):
		result.append(galoisMultiplication(multiplier, int2bin(i)))
	return result


def mixColumns():
	equa = []
	result = ['' for i in xrange(blockSize)]
	tt2 = generateMultByValTruthTable('02')
	tt3 = generateMultByValTruthTable('03')
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


def invMixColumns():
	equa = []
	result = ['' for i in xrange(blockSize)]
	tt0b = generateMultByValTruthTable('0b')
	tt0d = generateMultByValTruthTable('0d')
	tt09 = generateMultByValTruthTable('09')
	tt0e = generateMultByValTruthTable('0e')

	mt0b = generateMoebiusTransform(tt0b)
	mt0d = generateMoebiusTransform(tt0d)
	mt09 = generateMoebiusTransform(tt09)
	mt0e = generateMoebiusTransform(tt0e)

	equations0b = generateEquaMonomes(mt0b)
	equations0d = generateEquaMonomes(mt0d)
	equations09 = generateEquaMonomes(mt09)
	equations0e = generateEquaMonomes(mt0e)

	equaAES0b = generateEquaMonomesAES(equations0b)
	equaAES0d = generateEquaMonomesAES(equations0d)
	equaAES09 = generateEquaMonomesAES(equations09)
	equaAES0e = generateEquaMonomesAES(equations0e)

	binMon0b = generateBinaryMonomes(equaAES0b)
	binMon0d = generateBinaryMonomes(equaAES0d)
	binMon09 = generateBinaryMonomes(equaAES09)
	binMon0e = generateBinaryMonomes(equaAES0e)
	bits = generateAllBits()

	for cpt in xrange(4):
		for i in xrange(octetSize):
			val = i + (cpt*32)
			result[val] = binMon0e[val] + binMon0b[val+8] + binMon0d[val+16] + binMon09[val+24]
			result[val+8] = binMon09[val] + binMon0e[val+8] + binMon0b[val+16] + binMon0d[val+24]
			result[val+16] = binMon0d[val] + binMon09[val+8] + binMon0e[val+16] + binMon0b[val+24]
			result[val+24] = binMon0b[val] + binMon0d[val+8] + binMon09[val+16] + binMon0e[val+24]

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
