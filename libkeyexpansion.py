
from multiprocessing import Pool
from libmain import *

# calculation time
# simple process = 1690seconds * 25


sbox = [['63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '01', '67', '2b', 'fe', 'd7', 'ab', '76'],
	['ca', '82', 'c9', '7d', 'fa', '59', '47', 'f0', 'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0'],
	['b7', 'fd', '93', '26', '36', '3f', 'f7', 'cc', '34', 'a5', 'e5', 'f1', '71', 'd8', '31', '15'],
	['04', 'c7', '23', 'c3', '18', '96', '05', '9a', '07', '12', '80', 'e2', 'eb', '27', 'b2', '75'],
	['09', '83', '2c', '1a', '1b', '6e', '5a', 'a0', '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84'],
	['53', 'd1', '00', 'ed', '20', 'fc', 'b1', '5b', '6a', 'cb', 'be', '39', '4a', '4c', '58', 'cf'],
	['d0', 'ef', 'aa', 'fb', '43', '4d', '33', '85', '45', 'f9', '02', '7f', '50', '3c', '9f', 'a8'],
	['51', 'a3', '40', '8f', '92', '9d', '38', 'f5', 'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2'],
	['cd', '0c', '13', 'ec', '5f', '97', '44', '17', 'c4', 'a7', '7e', '3d', '64', '5d', '19', '73'],
	['60', '81', '4f', 'dc', '22', '2a', '90', '88', '46', 'ee', 'b8', '14', 'de', '5e', '0b', 'db'],
	['e0', '32', '3a', '0a', '49', '06', '24', '5c', 'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79'],
	['e7', 'c8', '37', '6d', '8d', 'd5', '4e', 'a9', '6c', '56', 'f4', 'ea', '65', '7a', 'ae', '08'],
	['ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6', 'e8', 'dd', '74', '1f', '4b', 'bd', '8b', '8a'],
	['70', '3e', 'b5', '66', '48', '03', 'f6', '0e', '61', '35', '57', 'b9', '86', 'c1', '1d', '9e'],
	['e1', 'f8', '98', '11', '69', 'd9', '8e', '94', '9b', '1e', '87', 'e9', 'ce', '55', '28', 'df'],
	['8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', '0f', 'b0', '54', 'bb', '16']]


def hex2binBlock(h):
	"""Returns the string of octetSize bits representation of hexadecimal h.
	usage: hex2bin('09cf4f3c') --> 00001001110011110100111100111100"""
	tmp = ''
	h = bin(int(h, 16)).lstrip('0b')
	for cpt in xrange(blockSize-len(h)):
		tmp += '0'
	for b in h:
		tmp += b
	return tmp


def binWord2hex(b):
	"""Returns the string of the hexadecimal representation of binary b.
	usage: bin2hex('00001001110011110100111100111100') --> 09cf4f3c"""
	tmp = []
	val = ''
	result = ''
	for i in xrange(wordSize):
		if (i % octetSize == 0) and (i <> 0):
			tmp.append(val)
			val = ''
		val += b[i]
	tmp.append(val)
	for byte in tmp:
		i = int(byte, 2)
		if (i == 0):
			buff = '00'
		elif ( i < 16):
			buff = '0' + hex(i).lstrip('0x')
		else:
			buff = hex(i).lstrip('0x').rstrip('L')
		result += buff
	return result


def getIndex(bit):
	result = 0
	val = int(bit.split('_')[1])
	for i in range(128):
		if i%8==0:
			if val in list(range(i,i+8)): result = i
	return result


def wordToByte(w):
	result = []
	result.append(w[0:8])
	result.append(w[8:16])
	result.append(w[16:24])
	result.append(w[24:32])
	return result


def byteToWord(w):
	result = []
	for i in xrange(4):
		for j in xrange(octetSize):
			result.append(w[i][j])
	return result


def generateSboxTruthTable():
	"""Returns the truth table of SBOX."""
	result = []
	for i in range(2**octetSize):
		tmp = int2hex(i)
		result.append(hex2bin(sbox[int(tmp[0], 16)][int(tmp[1], 16)]))
	return result


def generateSboxTruthWithRconTable(rcon):
	"""Returns the truth table of SBOX xored by RCON."""
	result = []
	for i in range(2**octetSize):
		tmp = int2hex(i)
		sb = sbox[int(tmp[0], 16)][int(tmp[1], 16)]
		rc = int2hex(int(sb, 16)^int(rcon, 16))
		result.append(hex2bin(rc))
	return result


def rotWord(w):
	w = wordToByte(w)
	result = []
	result.append(w[1])
	result.append(w[2])
	result.append(w[3])
	result.append(w[0])
	result = byteToWord(result)
	return result


def fixIndexEqua(equa, index):
	result = []
	for i in xrange(octetSize):
		temp = ''
		elt = 0
		while elt < len(equa[i]):
			if (equa[i][elt] == '_'):
				temp += '_'
				temp += str(int(equa[i][elt+1])+index)
				elt += 2
			else:
				temp += equa[i][elt]
				elt += 1
		result.append(temp)
	return result


def subWord(w, rcon):
	w = wordToByte(w)
	result = []
	tt = generateSboxTruthTable()
	mt = generateMoebiusTransform(tt)
	equations = generateEquaMonomes(mt)

	tt_rc = generateSboxTruthWithRconTable(rcon)
	mt_rc = generateMoebiusTransform(tt_rc)
	equations_rc = generateEquaMonomes(mt_rc)

	cpt = 0
	for cpt in xrange(4):
		tmp = []
		index = getIndex(w[cpt][0].split('+')[0])
		if cpt==0:
			subByte = fixIndexEqua(equations_rc, index)
		else:
			subByte = fixIndexEqua(equations, index)
		for i in xrange(octetSize):
			tmp.append(subByte[i])
		result.append(tmp)

	result = byteToWord(result)
	return result


def xorWords(w1, w2):
	result = []
	for i in xrange(wordSize):
		result.append(w1[i] + '+' + w2[i])
	return result


def generateW0():
	return generateGenericWord(wordSize*0, 'x')


def generateW1():
	return generateGenericWord(wordSize*1, 'x')


def generateW2():
	return generateGenericWord(wordSize*2, 'x')


def generateW3():
	return generateGenericWord(wordSize*3, 'x')


def generateW4():
	w4 = generateW3()
	w4 = rotWord(w4)
	w4 = subWord(w4, '01')
	w0 = generateW0()
	w4 = xorWords(w4, w0)
	return w4


def generateW5():
	w5 = generateW4()
	w1 = generateW1()
	w5 = xorWords(w5, w1)
	return w5


def generateW6():
	w6 = generateW5()
	w2 = generateW2()
	w6 = xorWords(w6, w2)
	return w6


def generateW7():
	w7 = generateW6()
	w3 = generateW3()
	w7 = xorWords(w7, w3)
	return w7


def generateW8():
	w8 = generateW3()
	w8 = rotWord(w8)
	w8 = subWord(w8, '02')
	w0 = generateW0()
	w8 = xorWords(w8, w0)
	return w8


def generateW9():
	w9 = generateW8()
	w1 = generateW1()
	w9 = xorWords(w9, w1)
	return w9


def generateW10():
	w10 = generateW9()
	w2 = generateW2()
	w10 = xorWords(w10, w2)
	return w10


def generateW11():
	w11 = generateW10()
	w3 = generateW3()
	w11 = xorWords(w11, w3)
	return w11


def generateW12():
	w12 = generateW3()
	w12 = rotWord(w12)
	w12 = subWord(w12, '04')
	w0 = generateW0()
	w12 = xorWords(w12, w0)
	return w12


def generateKn(w0, w1, w2, w3):
	result = []
	for bit in w0: result.append(bit)
	for bit in w1: result.append(bit)
	for bit in w2: result.append(bit)
	for bit in w3: result.append(bit)
	return result







def testWord(w, key):
	result = ''
	k = hex2binBlock(key)
	print k, key
	for i in xrange(wordSize):
		tmp = []
		bit = w[i].split('+')
		for monome in bit:
			m = monome.split('x_')
			if len(m) == 1:
				tmp.append('1')
			else:
				t = ''
				for j in xrange(1,len(m)):
					t += k[int(m[j])]
				tmp.append(t)
		r = []
		for item in tmp:
			r.append(str(reduce(lambda x, y: int(x)&int(y), item)))
		result += str(reduce(lambda x, y: int(x)^int(y), r))
	print result, binWord2hex(result)






