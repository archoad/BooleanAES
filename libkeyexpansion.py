

from libmain import *




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


rconList = ['01', '02', '04', '08', '10', '20', '40', '80', '1b', '36']


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


def generateWord(num):
	if (num < 4):
		w = generateGenericWord(wordSize*num, 'x')
	if (num >= 4):
		if ((num % 4) == 0):
			w = generateWord(3)
			w = rotWord(w)
			w = subWord(w, rconList[(num/4)-1])
			w = xorWords(w, generateWord(0))
		else:
			w = generateWord(num-1)
			w = xorWords(w, generateWord(num%4))
	return w


def generateKn(w0, w1, w2, w3):
	result = []
	for bit in w0: result.append(bit)
	for bit in w1: result.append(bit)
	for bit in w2: result.append(bit)
	for bit in w3: result.append(bit)
	return result


def testKeyExpansion():
	testWord(generateWord(4), '2b7e151628aed2a6abf7158809cf4f3c') # R0 key (w0, w1, w2, w3)
	testWord(generateWord(8), 'a0fafe1788542cb123a339392a6c7605') # R1 key (w4, w5, w6, w7)
	testWord(generateWord(12), 'f2c295f27a96b9435935807a7359f67f') # R2 key (w8, w9, w10, w11)
	testWord(generateWord(16), '3d80477d4716fe3e1e237e446d7a883b') # R3 key (w12, w13, w14, w15)
	testWord(generateWord(20), 'ef44a541a8525b7fb671253bdb0bad00') # R4 key (w16, w17, w18, w19)
	testWord(generateWord(24), 'd4d1c6f87c839d87caf2b8bc11f915bc') # R5 key (w20, w21, w22, w23)
	testWord(generateWord(28), '6d88a37a110b3efddbf98641ca0093fd') # R6 key (w24, w25, w26, w27)
	testWord(generateWord(32), '4e54f70e5f5fc9f384a64fb24ea6dc4f') # R7 key (w28, w29, w30, w31)
	testWord(generateWord(36), 'ead27321b58dbad2312bf5607f8d292f') # R8 key (w32, w33, w34, w35)
	testWord(generateWord(40), 'ac7766f319fadc2128d12941575c006e') # R9 key (w36, w37, w38, w39)


def testWord(w, key):
	result = ''
	k = largeHex2Bin(key)
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
	print result, wordBin2hex(result)


def addRoundKey(numRound, val):
	printColor('## AddRoundKey%s' % numRound, GREEN)
	fname = (fileNameEnc if val == 'enc' else fileNameDec)
	result = []
	if numRound == 0:
		result = generateKn(generateWord(0), generateWord(1), generateWord(2), generateWord(3))
	elif numRound == 1:
		result = generateKn(generateWord(4), generateWord(5), generateWord(6), generateWord(7))
	elif numRound == 2:
		result = generateKn(generateWord(8), generateWord(9), generateWord(10), generateWord(11))
	elif numRound == 3:
		result = generateKn(generateWord(12), generateWord(13), generateWord(14), generateWord(15))
	elif numRound == 4:
		result = generateKn(generateWord(16), generateWord(17), generateWord(18), generateWord(19))
	elif numRound == 5:
		result = generateKn(generateWord(20), generateWord(21), generateWord(22), generateWord(23))
	elif numRound == 6:
		result = generateKn(generateWord(24), generateWord(25), generateWord(26), generateWord(27))
	elif numRound == 7:
		result = generateKn(generateWord(28), generateWord(29), generateWord(30), generateWord(31))
	elif numRound == 8:
		result = generateKn(generateWord(32), generateWord(33), generateWord(34), generateWord(35))
	elif numRound == 9:
		result = generateKn(generateWord(36), generateWord(37), generateWord(38), generateWord(39))
	elif numRound == 10:
		result = generateKn(generateWord(40), generateWord(41), generateWord(42), generateWord(43))
	binMon = generateBinaryMonomes(result)

	for i in xrange(blockSize):
		f = openFile(fname+'%s.txt' % intToThreeChar(i))
		f.write('## addRoundKey%s\n' % numRound)
		f.write(binMon[i])
		closeFile(f)
	return result
