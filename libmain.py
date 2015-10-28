

import os
import timeit


BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = xrange(30, 38)
octetSize = 8 # SBOX takes 8 bits as input
wordSize = 32
blockSize = 128 #16 for mini-aes and 128 for aes
directory = 'AES_files/'
fileNameEnc = 'f_enc_'
fileNameDec = 'f_dec_'


def hex2bin(h):
	"""Returns the string of octetSize bits representation of hexadecimal h.
	usage: hex2bin('ff') --> 11111111"""
	tmp = ''
	h = bin(int(h, 16)).lstrip('0b')
	for cpt in xrange(octetSize-len(h)):
		tmp += '0'
	for b in h:
		tmp += b
	return tmp


def wordHex2bin(h):
	"""Returns the string of wordSize bits representation of hexadecimal h.
	usage: hex2bin('01000000') --> 00000001000000000000000000000000"""
	tmp = ''
	h = bin(int(h, 16)).lstrip('0b')
	for cpt in xrange(wordSize-len(h)):
		tmp += '0'
	for b in h:
		tmp += b
	return tmp


def bin2byte(b):
	"""Returns the string of the byte (8 bits) representation of binary b.
	usage: bin2byte('10') --> 00000010"""
	tmp = ''
	if len(b) > 8:
		for cpt in xrange(len(b)-8,len(b)):
			tmp += b[cpt]
	else:
		for i in xrange(8-len(b)):
			tmp += '0'
		tmp = tmp + b
	return tmp


def int2bin(i):
	"""Returns the string of the 8 bits representation of integer i.
	usage: int2bin(255) --> 11111111"""
	tmp = ""
	i = bin(i).lstrip('0b')
	for cpt in xrange(octetSize-len(i)):
		tmp += '0'
	tmp = tmp + i
	return tmp


def int2hex(i):
	"""Returns the string of hexadecimal representation of integer i.
	usage: int2hex(254) --> fe"""
	tmp = ""
	if (i == 0):
		tmp = '00'
	elif ( i < 16):
		tmp = '0' + hex(i).lstrip('0x')
	else:
		tmp = hex(i).lstrip('0x').rstrip('L')
	return tmp


def bin2hex(b):
	"""Returns the string of the hexadecimal representation of binary b.
	usage: bin2hex('11111010') --> fa"""
	tmp = []
	val = ''
	result = ''
	for i in xrange(blockSize):
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


def bin2monome(b):
	"""Return the monomes corresponding to the binary.
	usage: bin2monome(00110001) = x_2+x_3+x_7"""
	result = ''
	for i in xrange(octetSize):
		if b[i] == '1':
			tmp = 'x_%s' % (i)
			result += tmp
	return result


def monome2bin(m):
	"""Return the binary corresponding to the monome.
	usage: monome2bin(x_2+x_3+x_7) = 001100010000...00000000000"""
	temp = m.split('x_')
	result = ''
	for i in xrange(128):
		if str(i) in temp:
			result += '1'
		else:
			result += '0'
	return result


def xorTab(t1, t2):
	"""Takes two tabs t1 and t2 of same lengths and returns t1 XOR t2."""
	result = ''
	for i in xrange(len(t1)):
		result += str(int(t1[i]) ^ int(t2[i]))
	return result


def xorList(mylist):
	result = mylist[0]
	cpt = 0
	for i in xrange(len(mylist)):
		if cpt < len(mylist)-1:
			result = xorTab(result, mylist[cpt+1])
		cpt += 1
	return result


def hexToBinBlock(h):
	result = ''
	for i in xrange(0,len(h),2):
		result += hex2bin(h[i] + h[i+1])
	return result


def galoisMultiplication(a, b):
	"""Multiply two polynoms in Rijndael's galois field.
	usage: galoisMultiplication('11110000', '10100111') = 01101011
	algorithm: http://www.samiam.org/galois.html"""
	product = '00000000'
	for i in xrange(octetSize):
		if int(b[7], 2) & 1: # low bit of b ist set
			product = bin2byte(bin(int(product, 2) ^ int(a, 2)).lstrip('0b'))
		aHighBit = int(a[0], 2) # aHighBit contains the high bit of a
		a = bin2byte(bin(int(a, 2) << 1).lstrip('0b')) # a is rotated one bit to the left
		if aHighBit & 1: # high bit of a is set
			num = hex2bin('1b')
			a = bin2byte(bin(int(a, 2) ^ int(num, 2)).lstrip('0b'))
		b = bin2byte(bin(int(b, 2) >> 1).lstrip('0b')) # b is rotated one bit to the right
	return product


def printColor(string, color=RED):
	print '\033[1;%dm%s\033[0m' % (color, string)


def intToThreeChar(i):
	"""Transform an integer to a 3 chars length string by adding 0
	uasge: intToThreeChar(12) return 012"""
	temp = str(i)
	result = ''
	if len(temp) == 1:
		result = '00' + temp
	elif len(temp) == 2:
		result = '0' + temp
	else:
		result = temp
	return result


def createFile(name):
	"""Create file named by "name" for data"""
	f = open(directory+name, 'w')
	return f


def openFile(name):
	"""Open file named by "name" for data"""
	f = open(directory+name, 'a')
	return f


def readFile(name):
	"""Read file called name and return a list in which one element corresponds to a line"""
	f = open(directory+name, 'r')
	result = f.readlines()
	closeFile(f)
	return result


def closeFile(f):
	"""Close file handled by f"""
	if not(f.closed):
		f.close()
	return 0


def generateEquaMonomes(mt):
	result = []
	for b in xrange(len(mt)):
		tmp = ''
		for i in xrange(len(mt[b])):
			if mt[b][i] == '1':
				if i == 0:
					tmp += '1+' # constant
				else:
					tmp += bin2monome(int2bin(i)) + '+'
		result.append(tmp.rstrip('+'))
	return result


def traiteMonomes(equa, cpt):
	result =''
	tmp = equa.split('+')
	for m in tmp:
		if m == '1':
			result += '1'
		else:
			t = m.split('x_')
			for item in t:
				if item <> '':
					result += 'x_' + str(int(item) + ((cpt-1)*octetSize))
		result += '+'
	return result.rstrip('+')


def generateEquaMonomesAES(equations):
	result = []
	cpt = 0
	for i in xrange(128):
		if i%octetSize == 0:
			cpt += 1
		result.append(traiteMonomes(equations[i%octetSize], cpt))
	return result


def moebiusTransform(tab):
	"""Takes a tab and return tab[0 : len(tab)/2], tab[0 : len(tab)/2] ^ tab[len(tab)/2 : len(tab)].
	usage: moebiusTransform(1010011101010100) --> [1100101110001010]"""
	if len(tab) == 1:
		return tab
	else:
		t1 = tab[0 : len(tab)/2]
		t2 = tab[len(tab)/2 : len(tab)]
		t2 = xorTab(t1, t2)
		t1 = moebiusTransform(t1)
		t2 = moebiusTransform(t2)
		t1 += t2
		return t1


def generateMoebiusTransform(tt):
	"""Creates octetSize strings, each containing the result of Moebius
	transform for a boolean function of tab. The result is a tab of octetSize
	cases each one containing 2**octetSize bits. Each case describe a bit of the function"""
	result = []
	for i in xrange(octetSize):
		tmp = ''
		for block in tt:
			tmp += block[i]
		result.append(moebiusTransform(tmp))
	return result


def generateBinaryMonomes(equations):
	result = []
	for i in xrange(len(equations)):
		temp = ''
		for monome in equations[i].split('+'):
			if monome == '1':
				temp += '1\t' + monome2bin('') + '\n'
			else:
				temp += '0\t' + monome2bin(monome) + '\n'
		result.append(temp)
	return result


def bitToLatex(bit):
	bit = bit.replace('+', ' \oplus ')
	bit = '$' + bit + '$'
	print bit


def createAESFiles(val):
	d = os.path.dirname(directory)
	if not os.path.exists(d):
		printColor('## Create directory %s' % (d), GREEN)
		os.mkdir(directory)
	else:
		printColor('## Directory %s already exist' % (d), RED)
	fname = (fileNameEnc if val == 'enc' else fileNameDec)
	for i in xrange(blockSize):
		f = createFile(fname+'%s.txt' % (intToThreeChar(i)))
		closeFile(f)
	return 1


def writeEndFlag(val):
	fname = (fileNameEnc if val == 'enc' else fileNameDec)
	for i in xrange(blockSize):
		f = openFile(fname+'%s.txt' % intToThreeChar(i))
		f.write('## end\n')
		closeFile(f)


def generateGenericWord(s, c):
	"""Generate a tab containing wordSize variables
	usage: generateGenericByte(0, 'x') return ['x_0', 'x_1', 'x_2', 'x_3', 'x_4', ..., 'x_30', 'x_31']"""
	result = []
	for i in xrange(s,wordSize+s):
		result.append('%s_%s' % (c, i))
	return result


def generateGenericBlock(c):
	"""Generate a tab containing blockSize variables
	usage: generateGenericBlock('x') return ['x_0', 'x_1', 'x_2', 'x_3', 'x_4', ..., 'x_126', 'x_127']"""
	result = []
	for i in xrange(blockSize):
		result.append('%s_%s' % (c, i))
	return result


def generateBitsBlock(c):
	"""Generate a string containing blockSize bits
	usage: generateGenericBlock('x_3') return 00010000000...00000"""
	result = ''
	tmp = int(c.split('_')[1])
	for i in xrange(blockSize):
		if i == tmp:
			result += '1'
		else:
			result += '0'
	return result


def generateAllBits():
	"""Generate a list containing 128 input corresponding to the
		conversion of integer to binary for i in xrange(blockSize)"""
	result = []
	tmp = []
	for i in xrange(blockSize):
		tmp.append('0')
	for i in xrange(blockSize):
		t = ''
		tmp[i] = '1'
		result.append('0\t' + t.join(tmp) + '\n')
		tmp[i] = '0'
	return result


def extractBlock(file, startBlock, endBlock):
	tmp = []
	flag = 0
	allLines = readFile(file)
	for line in allLines:
		line = line.rstrip('\n')
		if line == startBlock: flag = 1
		if line == endBlock: flag = 0
		if flag:
			if line[0] <> '#':
				tmp.append(line)
	return tmp


def displayTruthTable(tt):
	for i in xrange(len(tt)):
		print i, '\t', int(tt[i], 2), '\t', int2bin(i), '\t', tt[i]


def displayEqua(tt):
	mt = generateMoebiusTransform(tt)
	equa = generateEquaMonomes(mt)
	for i in xrange(octetSize):
		equa2sagemath(equa[i])
		print i, '\t', equa2sagemath(equa[i])




