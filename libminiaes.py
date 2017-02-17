

nibbleSize = 4 # a nibble is 4 bits length
blockSize = 2**nibbleSize # in mini-aes a block is 4 nibbles length

int2hex = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E' , 'F']


sbox = [
	'1110',
	'0100',
	'1101',
	'0001',
	'0010',
	'1111',
	'1011',
	'1000',
	'0011',
	'1010',
	'0110',
	'1100',
	'0101',
	'1001',
	'0000',
	'0111',
	]


gf24mult = [
	'0000000000000000',
	'0123456789ABCDEF',
	'02468ACE3175B9FD',
	'0365CFA9B8DE7412',
	'048C37BF62EA51D9',
	'05AF72D8EB419C36',
	'06CABD71539FE824',
	'07E9F816DA3425CB',
	'083B6E5DC4F7A291',
	'09182B3A4D5C6F7E',
	'0A7DE493F5821B6C',
	'0B5EA1F47C29D683',
	'0CB759E2A61DF348',
	'0D941C852FB63EA7',
	'0EF1D32C97684AB5',
	'0FD296481EC3875A'
	]




def intToNibble(i):
	"""Returns the string of nibbleSize bits representation of integer i.
	usage: intToNibble(15) --> 1111"""
	tmp = ''
	i = bin(i).lstrip('0b')
	for cpt in range(nibbleSize-len(i)):
		tmp += '0'
	for b in i:
		tmp += b
	return tmp


def hexToNibble(h):
	"""Returns the string of nibbleSize bits representation of hexadecimal h.
	usage: hexToNibble(F) --> 1111"""
	return intToNibble(int(h, 16))


def intToBinOctect(i):
	"""Returns the string of the 8 bits representation of integer i.
	usage: intToBinOctect(134) --> 10000110"""
	tmp = ""
	i = bin(i).lstrip('0b')
	for cpt in range(8-len(i)):
		tmp += '0'
	tmp = tmp + i
	return tmp


def intToBinBlock(i):
	"""Returns the string of the 16 bits representation of integer i.
	usage: intToBinBlock(65523) --> 1111111111110011"""
	tmp = ""
	i = bin(i).lstrip('0b')
	for cpt in range(16-len(i)):
		tmp += '0'
	tmp = tmp + i
	return tmp


def nibbleToInt(nibble):
	"""Returns a string of the integer representation for a nibbleSize bits.
	usage: nibbleToInt(1111) --> 15"""
	result = 0
	for i in range(len(nibble)):
		result += int(nibble[i]) * 2**(len(nibble)-(i+1))
	return result


def nibbleToHex(nibble):
	"""Returns a string of the hexadecimal representation for a nibbleSize bits.
	usage: nibbleToInt(1111) --> F"""
	return int2hex[nibbleToInt(nibble)]


def blockToNibbles(block):
	""" Take a string of blockSize and return blockSize/nibbleSize strings of nibbleSize.
	usage: blockToNibbles([1001110001100011) --> 1001 1100 0110 0011 """
	result = ''
	tmp = ''
	for cpt in range(len(block)):
		if not(cpt % nibbleSize) and (cpt != 0):
			result += tmp +' '
			tmp = ''
		tmp += block[cpt]
	result += tmp
	return result.lstrip(' ')


def mapSbox(nibble):
	return sbox[nibbleToInt(nibble)]


def xorTab(t1, t2):
	"""Takes two tabs t1 and t2 of same lengths and returns t1 XOR t2."""
	result = ''
	for i in range(len(t1)):
		result += str(int(t1[i]) ^ int(t2[i]))
	return result


def xorList(mylist):
	result = mylist[0]
	cpt = 0
	for i in range(len(mylist)):
		if cpt < len(mylist)-1:
			result = xorTab(result, mylist[cpt+1])
		cpt += 1
	return result



def equaToLatex(equa, letter, num):
	result = '$'
	for monomial in equa.split('+'):
		if monomial == '1':
			result += monomial + '+'
		else:
			for val in monomial.split('x'):
				if val != '':
					if (num):
						result += '%s_{%s,%s}' % (letter, num, val)
					else:
						result += '%s_{%s}' % (letter, val)
			result += '+'
	result = result.rstrip('+') + '$'
	result = result.replace('+', ' \oplus ')
	return result


def moebiusTransform(tab):
	"""Takes a tab and return tab[0 : len(tab)/2], tab[0 : len(tab)/2] ^ tab[len(tab)/2 : len(tab)].
	usage: moebiusTransform(1010011101010100) --> [1100101110001010]"""
	if len(tab) == 1:
		return tab
	else:
		t1 = tab[0 : int(len(tab)/2)]
		t2 = tab[int(len(tab)/2) : len(tab)]
		t2 = xorTab(t1, t2)
		t1 = moebiusTransform(t1)
		t2 = moebiusTransform(t2)
		t1 += t2
		return t1


def generateMoebiusTransform(tab):
	"""Creates blockSize strings, each containing the result of Moebius Transform for a boolean function of tab.
	The result is a tab of 16 cases each one containing 65536 bits. Each case describe a bit of the function"""
	result = []
	for i in range(blockSize):
		tmp = ''
		for block in tab:
			tmp += block[i]
		result.append(moebiusTransform(tmp))
	return result


def definesMonomeBlock(mt):
	"""Takes a moebius transform table and calulates corresponding monome.
	Scale is for block of 16 bits (a mini-aes block)"""
	tab = []
	equa = ''
	for i in range(2**blockSize):
		if mt[i] == '1':
			tmp = intToBinBlock(i)
			if i == 0:
				tab.append('1') # constant
			else:
				monome = ''
				for bit in range(blockSize):
					if tmp[bit] == '1':
						monome += 'x' + str(bit+1)
				tab.append(monome)
		else:
			tab.append('\t')
	for i in range(2**blockSize):
		if tab[i] != '\t':
			equa += tab[i] + '+'
	return(equa.rstrip('+'))


def gf24Multiply(n1, n2):
	"""Returns the string of nibbleSize bits representation of n1xn2 in GF24 (modulo x4+x+1).
	usage: gf2Multiply('1111', '0000') --> '1111' """
	i1 = nibbleToInt(n1)
	i2 = nibbleToInt(n2)
	return hexToNibble(gf24mult[i1][i2])


def generateNibbleSubTruthTable():
	"""Returns the truth table of the mini aes NibbleSub function."""
	result = []
	for i in range(2**blockSize):
		tmp = map(mapSbox, blockToNibbles(intToBinBlock(i)).split(' '))
		result.append(''.join(tmp))
	return result


def generateShiftRowTruthTable():
	"""Returns the truth table of the mini aes ShiftRow function."""
	result = []
	for i in range(2**blockSize):
		tmp = []
		tabBlock = blockToNibbles(intToBinBlock(i)).split(' ')
		tmp.append(tabBlock[0])
		tmp.append(tabBlock[3])
		tmp.append(tabBlock[2])
		tmp.append(tabBlock[1])
		result.append(''.join(tmp))
	return result


def generateMixColumnsTruthTable():
	"""Returns the truth table of the mini aes MixColumns function.
		d0 =(0011 x c0) + (0010 x c1)
		d1 =(0010 x c0) + (0011 x c1)
		d2 =(0011 x c2) + (0010 x c3)
		d3 =(0010 x c2) + (0011 x c3)"""
	result = []
	for i in range(2**blockSize):
		tmp = blockToNibbles(intToBinBlock(i)).split(' ')
		c0 = tmp[0]
		c1 = tmp[1]
		c2 = tmp[2]
		c3 = tmp[3]
		d0 = xorTab(gf24Multiply('0011', c0), gf24Multiply('0010', c1))
		d1 = xorTab(gf24Multiply('0010', c0), gf24Multiply('0011', c1))
		d2 = xorTab(gf24Multiply('0011', c2), gf24Multiply('0010', c3))
		d3 = xorTab(gf24Multiply('0010', c2), gf24Multiply('0011', c3))
		result.append(d0 + d1 + d2 + d3)
	return result


def generateRoundsKeysTruthTable():
	"""Returns the truth table of the mini aes rounds keys."""
	k0 = []
	k1 = []
	k2 = []
	for i in range(2**blockSize):
		tmp = blockToNibbles(intToBinBlock(i)).split(' ')
		w0 = tmp[0]
		w1 = tmp[1]
		w2 = tmp[2]
		w3 = tmp[3]
		w4 = xorTab( xorTab(sbox[nibbleToInt(w3)], '0001'), w0)
		w5 = xorTab(w1, w4)
		w6 = xorTab(w2, w5)
		w7 = xorTab(w3, w6)
		w8 = xorTab( xorTab(sbox[nibbleToInt(w7)], '0010'), w4)
		w9 = xorTab(w5, w8)
		w10 = xorTab(w6, w9)
		w11 = xorTab(w7, w10)
		k0.append(w0 + w1 + w2 + w3)
		k1.append(w4 + w5 + w6 + w7)
		k2.append(w8 + w9 + w10 + w11)
	return(k0, k1, k2)


def generateRoundOneTruthTable():
	"""Returns the truth table of the mini aes first round.
	Equation is C = NS + SR + MC"""
	result = []
	ns_tt = generateNibbleSubTruthTable()
	sr_tt = generateShiftRowTruthTable()
	mc_tt = generateMixColumnsTruthTable()
	for i in range(2**blockSize):
		tmp = mc_tt[ int(sr_tt[ int(ns_tt[i], 2) ], 2) ]
		result.append(tmp)
	return result


def generateRoundTwoTruthTable():
	"""Returns the truth table of the mini aes second round.
	Equation is C = NS + SR"""
	result = []
	ns_tt = generateNibbleSubTruthTable()
	sr_tt = generateShiftRowTruthTable()
	for i in range(2**blockSize):
		tmp = sr_tt[ int(ns_tt[i], 2) ]
		result.append(tmp)
	return result
