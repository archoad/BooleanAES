

from libmain import *


def bin2byte(b):
	"""Returns the string of the byte (8 bits) representation of binary b.
	usage: bin2byte('10') --> 00000010"""
	tmp = ''
	if len(b) > 8:
		for cpt in range(len(b)-8,len(b)):
			tmp += b[cpt]
	else:
		for i in range(8-len(b)):
			tmp += '0'
		tmp = tmp + b
	return tmp


def galoisMultiplication(a, b):
	"""Multiply two polynoms in Rijndael's galois field.
	usage: galoisMultiplication('11110000', '10100111') = 01101011
	algorithm: http://www.samiam.org/galois.html"""
	product = '00000000'
	for i in range(octetSize):
		if int(b[7], 2) & 1: # low bit of b ist set
			product = bin2byte(bin(int(product, 2) ^ int(a, 2)).lstrip('0b'))
		aHighBit = int(a[0], 2) # aHighBit contains the high bit of a
		a = bin2byte(bin(int(a, 2) << 1).lstrip('0b')) # a is rotated one bit to the left
		if aHighBit & 1: # high bit of a is set
			num = hex2bin('1b')
			a = bin2byte(bin(int(a, 2) ^ int(num, 2)).lstrip('0b'))
		b = bin2byte(bin(int(b, 2) >> 1).lstrip('0b')) # b is rotated one bit to the right
	return product


def generateMultBy02TruthTable():
	result = []
	multiplier = hex2bin('02')
	for i in range(2**octetSize):
		result.append(galoisMultiplication(multiplier, int2bin(i)))
	return result


def generateMultBy03TruthTable():
	result = []
	multiplier = hex2bin('03')
	for i in range(2**octetSize):
		result.append(galoisMultiplication(multiplier, int2bin(i)))
	return result
