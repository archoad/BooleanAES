

from libmain import *


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
