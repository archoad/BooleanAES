

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = xrange(30, 38)
octetSize = 8 # SBOX takes 8 bits as input
blockSize = 128 #16 for mini-aes and 128 for aes
directory = 'AES_files/'


def hex2bin(h):
	"""Returns the string of octetSize bits representation of hexadecimal h.
	usage: hex2bin(ff) --> 11111111"""
	tmp = ''
	h = bin(int(h, 16)).lstrip('0b')
	for cpt in xrange(octetSize-len(h)):
		tmp += '0'
	for b in h:
		tmp += b
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
	global directory
	f = open(directory+name, 'w')
	return f


def openFile(name):
	"""Open file named by "name" for data"""
	global directory
	f = open(directory+name, 'a')
	return f


def readFile(name):
	"""Read file called name and return a list in which one element corresponds to a line"""
	global directory
	f = open(directory+name, 'r')
	result = f.readlines()
	closeFile(f)
	return result


def closeFile(f):
	"""Close file handled by f"""
	if not(f.closed):
		f.close()
	return 0


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
	"""Creates octetSize strings, each containing the result of Moebius transform for a boolean function of tab."""
	result = []
	for i in xrange(octetSize):
		tmp = ''
		for block in tt:
			tmp += block[i]
		result.append(moebiusTransform(tmp))
	return result


def bitToLatex(bit):
	bit = bit.replace('+', ' \oplus ')
	bit = '$' + bit + '$'
	print bit

