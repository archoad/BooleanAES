#! /usr/bin/env python
# -*- coding: utf-8 -*-


sbox = [
	[1, 1, 1, 0],
	[0, 1, 0, 0],
	[1, 1, 0, 1],
	[0, 0, 0, 1],
	[0, 0, 1, 0],
	[1, 1, 1, 1],
	[1, 0, 1, 1],
	[1, 0, 0, 0],
	[0, 0, 1, 1],
	[1, 0, 1, 0],
	[0, 1, 1, 0],
	[1, 1, 0, 0],
	[0, 1, 0, 1],
	[1, 0, 0, 1],
	[0, 0, 0, 0],
	[0, 1, 1, 1],
]


invsbox = [
	[1, 1, 1, 0],
	[0, 0, 1, 1],
	[0, 1, 0, 0],
	[1, 0, 0, 0],
	[0, 0, 0, 1],
	[1, 1, 0, 0],
	[1, 0, 1, 0],
	[1, 1, 1, 1],
	[0, 1, 1, 1],
	[1, 1, 0, 1],
	[1, 0, 0, 1],
	[0, 1, 1, 0],
	[1, 0, 1, 1],
	[0, 0, 1, 0],
	[0, 0, 0, 0],
	[0, 1, 0, 1],
]


h2b = {"0":[0, 0, 0, 0], "1":[0, 0, 0, 1], "2":[0, 0, 1, 0], "3":[0, 0, 1, 1],
		"4":[0, 1, 0, 0], "5":[0, 1, 0, 1], "6":[0, 1, 1, 0], "7":[0, 1, 1, 1],
		"8":[1, 0, 0, 0], "9":[1, 0, 0, 1], "a":[1, 0, 1, 0], "b":[1, 0, 1, 1],
		"c":[1, 1, 0, 0], "d":[1, 1, 0, 1], "e":[1, 1, 1, 0], "f":[1, 1, 1, 1]}


multGF24 = [
['0000000000000000'],
['0123456789abcdef'],
['02468ace3175b9fd'],
['0365cfa9b8de7412'],
['048c37bf62ea51d9'],
['05af72d8eb419c36'],
['06cabd71539fe824'],
['07e9f816da3425cb'],
['083b6e5dc4f7a291'],
['09182b3a4d5c6f7e'],
['0a7de493f5821b6c'],
['0b5ea1f47c29d683'],
['0cb759e2a61df348'],
['0d941c852fb63ea7'],
['0ef1d32c97684ab5'],
['0fd296481ec3875a']]


def c2h(char):
	return hex(int(ord(char))).lstrip('0x')


def stringToBlocks(str):
	""" This function take a char as input and
	return a matrix of nibbles.
	sample: stringToBlocks('t') -> [[[0, 1, 1, 1], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 1, 1]]]"""
	result = []
	if (len(str) % 2):
		str = str + '#'
	for cpt in range(0, len(str), 2):
		result.append([h2b[c2h(str[cpt])[0]], h2b[c2h(str[cpt])[1]], h2b[c2h(str[cpt+1])[0]], h2b[c2h(str[cpt+1])[1]]])
	return result


def blocksToBin(blocks):
	result = ''
	for block in blocks:
		result += nibblesToString(block)
	print result


def blocksToString(blocks):
	tmp = ''
	result = ''
	for block in blocks:
		for nibble in block:
			i = nibbleToInt(nibble)
			if (i):
				tmp += hex(i).lstrip('0x')
			else:
				tmp += '0'
	for i in range(0, len(tmp), 2):
		result += chr(int(tmp[i]+tmp[i+1], 16))
	return result


def nibblesToBlock(nibbles):
	""" This function take a list of 4 nibbles as input
	and return a list (block) of 16 binary digit.
	"""
	result = []
	for n in nibbles:
		for bit in n:
			result.append(bit)
	return result


def nibblesToString(nibbles):
	"""
	This function take a list of 4 nibbles as input
	and return a string for printing these nibbles.
	"""
	result = ''
	for n in nibbles:
		for bit in n:
			result += str(bit)
		result += ' '
	return result


def nibbleToInt(nibble):
	""" This function take a single nibble
	as input and return its integer representation.
	"""
	result = (nibble[0] * 2**3) + (nibble[1] * 2**2) + (nibble[2] * 2**1) + (nibble[3] * 2**0)
	return result


def xorNibbles(n1, n2):
	""" This function take two nibbles as input,
	execute a xor operation and return the result.
	"""
	result = []
	for i in range(4):
		result.append(n1[i] ^ n2[i])
	return result


def galoisMultNibbles(n1, n2):
	""" This function take two nibbles
	as input, execute their galois multiplication
	and return the result.
	For mini aes galois multiplication means n1 * n2 mod(x^4 + x +1);
	"""
	i1 = nibbleToInt(n1)
	i2 = nibbleToInt(n2)
	return h2b[multGF24[i1][0][i2]]


def keySchedule(key):
	""" This function take a key in the form
	of a list of four nibbles, execute the mini aes
	key schedule and return the result.
	"""
	rcon1 = [0, 0, 0, 1]
	rcon2 = [0, 0, 1, 0]
	w0 = key[0]
	w1 = key[1]
	w2 = key[2]
	w3 = key[3]
	w4 = xorNibbles(xorNibbles(w0, sbox[nibbleToInt(w3)]), rcon1)
	w5 = xorNibbles(w1, w4)
	w6 = xorNibbles(w2, w5)
	w7 = xorNibbles(w3, w6)
	w8 = xorNibbles(xorNibbles(w4, sbox[nibbleToInt(w7)]), rcon2)
	w9 = xorNibbles(w5, w8)
	w10 = xorNibbles(w6, w9)
	w11 = xorNibbles(w7, w10)
	return [[w0, w1, w2, w3], [w4, w5, w6, w7], [w8, w9, w10, w11]]


def addKey(key, nibbles):
	result = []
	for i in range(4):
		result.append( xorNibbles(nibbles[i], key[i]) )
	print "addKey ->\t", nibblesToString(result)
	return result


def nibbleSub(nibbles):
	result = []
	for n in nibbles:
		tmp = (n[0] * 2**3) + (n[1] * 2**2) + (n[2] * 2**1) + (n[3] * 2**0)
		result.append(sbox[tmp])
	print "nibbleSub ->\t", nibblesToString(result)
	return result


def invNibbleSub(nibbles):
	result = []
	for n in nibbles:
		tmp = (n[0] * 2**3) + (n[1] * 2**2) + (n[2] * 2**1) + (n[3] * 2**0)
		result.append(invsbox[tmp])
	print "invNibbleSub ->\t", nibblesToString(result)
	return result


def shiftRow(nibbles):
	result = []
	result.append(nibbles[0])
	result.append(nibbles[3])
	result.append(nibbles[2])
	result.append(nibbles[1])
	print "shiftRow ->\t", nibblesToString(result)
	return result


def mixColumn(nibbles):
	matrix = [[0, 0, 1, 1], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 1]]
	d0 = xorNibbles(galoisMultNibbles(matrix[0], nibbles[0]), galoisMultNibbles(matrix[2], nibbles[1]))
	d1 = xorNibbles(galoisMultNibbles(matrix[1], nibbles[0]), galoisMultNibbles(matrix[3], nibbles[1]))
	d2 = xorNibbles(galoisMultNibbles(matrix[0], nibbles[2]), galoisMultNibbles(matrix[2], nibbles[3]))
	d3 = xorNibbles(galoisMultNibbles(matrix[1], nibbles[2]), galoisMultNibbles(matrix[3], nibbles[3]))
	result = [d0, d1, d2, d3]
	print "mixColumn ->\t", nibblesToString(result)
	return result


def miniAESencrypt(plain, key):
	print "### plain ->\t", nibblesToString(plain)
	print "### key ->\t", nibblesToString(key)
	roundKeys = keySchedule(key)
	cipher = addKey(roundKeys[0], plain)
	cipher = nibbleSub(cipher)
	cipher = shiftRow(cipher)
	cipher = mixColumn(cipher)
	cipher = addKey(roundKeys[1], cipher)
	cipher = nibbleSub(cipher)
	cipher = shiftRow(cipher)
	cipher = addKey(roundKeys[2], cipher)
	print "### cipher ->\t", nibblesToString(cipher)
	return cipher


def miniAESdecrypt(cipher, key):
	print "### cipher ->\t", nibblesToString(cipher)
	print "### key ->\t", nibblesToString(key)
	roundKeys = keySchedule(key)
	plain = addKey(roundKeys[2], cipher)
	plain = invNibbleSub(plain)
	plain = shiftRow(plain)
	plain = addKey(roundKeys[1], plain)
	plain = mixColumn(plain)
	plain = invNibbleSub(plain)
	plain = shiftRow(plain)
	plain = addKey(roundKeys[0], plain)
	print "### plain ->\t", nibblesToString(plain)
	return plain


def miniAEStextEncrypt(plain, key):
	print plain, key
	cipher = []
	binplain = stringToBlocks(plain)
	binkey = stringToBlocks(key)
	for block in binplain:
		cipher.append(miniAESencrypt(block, binkey[0]))
	return cipher


def miniAEStextDecrypt(cipher, key):
	print cipher, key
	plain = []
	binkey = stringToBlocks(key)
	for block in cipher:
		plain.append(miniAESdecrypt(block, binkey[0]))
	return blocksToString(plain).rstrip('#')


def miniAESvectorTest():
	plain = [[1, 0, 0, 1], [1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1]]
	key =   [[1, 1, 0, 0], [0, 0, 1, 1], [1, 1, 1, 1], [0, 0, 0, 0]]
	cipher = miniAESencrypt(plain, key)
	print
	plain = miniAESdecrypt(cipher, key)


def miniAEStextTest(key, plain):
	cipher = miniAEStextEncrypt(plain, key)
	plain = miniAEStextDecrypt(cipher, key)
	print plain





if __name__ == "__main__":
	miniAESvectorTest()
	print
	miniAEStextTest('KE', 'ab')