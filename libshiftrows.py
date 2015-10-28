

from libmain import *




def shiftRows():
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
		for bit in xrange(blockSize):
			if SR[i][bit] == '1':
				equa.append('x_%s' % (bit))
	return equa


def invShiftRows():
	Nb = 4
	result = []
	SR = []
	equa = []
	state = [[(i*Nb)+j for i in xrange(Nb)] for j in xrange(Nb)]
	tmp = [[0 for i in xrange(Nb)] for i in xrange(Nb)]
	for i in xrange(Nb):
		for j in xrange(Nb):
			tmp[i][(j + i) % Nb] = state[i][j]
	for row in xrange(Nb):
		for byte in xrange(Nb):
			result.append(tmp[byte][row])
	for numByte in result:
		for i in xrange(octetSize):
			SR.append(generateBitsBlock('x_' + str((numByte*octetSize)+i)))
	for i in xrange(blockSize):
		for bit in xrange(blockSize):
			if SR[i][bit] == '1':
				equa.append('x_%s' % (bit))
	return equa