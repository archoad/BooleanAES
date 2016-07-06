

from libmain import *




def shiftRows():
	Nb = 4
	result = []
	SR = []
	equa = []
	state = [[(i*Nb)+j for i in range(Nb)] for j in range(Nb)]
	tmp = [[0 for i in range(Nb)] for i in range(Nb)]
	for i in range(Nb):
		for j in range(Nb):
			tmp[i][j] = state[i][(j + i) % Nb]
	for row in range(Nb):
		for byte in range(Nb):
			result.append(tmp[byte][row])
	for numByte in result:
		for i in range(octetSize):
			SR.append(generateBitsBlock('x_' + str((numByte*octetSize)+i)))
	for i in range(blockSize):
		for bit in range(blockSize):
			if SR[i][bit] == '1':
				equa.append('x_%s' % (bit))
	return equa


def invShiftRows():
	Nb = 4
	result = []
	SR = []
	equa = []
	state = [[(i*Nb)+j for i in range(Nb)] for j in range(Nb)]
	tmp = [[0 for i in range(Nb)] for i in range(Nb)]
	for i in range(Nb):
		for j in range(Nb):
			tmp[i][(j + i) % Nb] = state[i][j]
	for row in range(Nb):
		for byte in range(Nb):
			result.append(tmp[byte][row])
	for numByte in result:
		for i in range(octetSize):
			SR.append(generateBitsBlock('x_' + str((numByte*octetSize)+i)))
	for i in range(blockSize):
		for bit in range(blockSize):
			if SR[i][bit] == '1':
				equa.append('x_%s' % (bit))
	return equa
