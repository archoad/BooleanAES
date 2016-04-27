

from libmain import *
from libsubbytes import *
from libshiftrows import *
from libmixcolumns import *
from libkeyexpansion import *


def writeInvSubBytes(numRound):
	printColor('## InvSubBytes %s' % numRound, GREEN)
	equa = invSubBytes()
	binMon = generateBinaryMonomes(equa)
	for i in xrange(blockSize):
		f = openFile(fileNameDec+'%s.txt' % intToThreeChar(i))
		f.write('## invSubBytes%s\n' % numRound)
		f.write(binMon[i])
		closeFile(f)
	return equa


def writeInvShiftRows(numRound):
	printColor('## InvShiftRows %s' % numRound, GREEN)
	equa = invShiftRows()
	binMon = generateBinaryMonomes(equa)
	for i in xrange(blockSize):
		f = openFile(fileNameDec+'%s.txt' % intToThreeChar(i))
		f.write('## invShiftRows%s\n' % numRound)
		f.write(binMon[i])
		closeFile(f)
	return equa


def writeInvMixColumns(numRound):
	printColor('## InvMixColumns %s' % numRound, GREEN)
	equa = invMixColumns()
	binMon = generateBinaryMonomes(equa)
	for i in xrange(blockSize):
		f = openFile(fileNameDec+'%s.txt' % intToThreeChar(i))
		f.write('## invMixColumns%s\n' % numRound)
		f.write(binMon[i])
		closeFile(f)
	return equa


def writeRoundDec(numRound, equaSB, equaSR):
	printColor('## Round %s' % numRound, GREEN)
	resultSR = []
	for i in xrange(blockSize):
		equaSR[i] = equaSR[i].split('_')
		resultSR.append(equaSB[int(equaSR[i][1])])
	binMon = generateBinaryMonomes(resultSR)

	for i in xrange(blockSize):
		f = openFile(fileNameDec+'%s.txt' % intToThreeChar(i))
		f.write('## Round%s\n' % numRound)
		f.write(binMon[i])
		closeFile(f)
	return resultSR


def generateDecStepsFiles():
	createAESFiles('dec')
	writeInvShiftRows(3)
	writeInvSubBytes(3)
	addRoundKey(3, 'dec')
	writeInvMixColumns(3)
	writeInvShiftRows(2)
	writeInvSubBytes(2)
	addRoundKey(2, 'dec')
	writeInvMixColumns(2)
	writeInvShiftRows(1)
	writeInvSubBytes(1)
	addRoundKey(1, 'dec')
	writeInvMixColumns(1)
	writeInvShiftRows(0)
	writeInvSubBytes(0)
	addRoundKey(0, 'dec')
	writeEndFlag('dec')
#	print currentStep, len(currentStep)
#	bitToLatex(currentStep[127])
	printColor('## Files generated', RED)


def controlDecStepsFiles():
	cipherBlock = '2d6d7ef03f33e334093602dd5bfb12c7'
	key = '000102030405060708090a0b0c0d0e0f'
	clearBlock = '00112233445566778899aabbccddeeff'

	printColor('## Cipher block %s' % (cipherBlock), BLUE)
	print largeHex2Bin(cipherBlock), len(largeHex2Bin(cipherBlock))
	printColor('## Key block %s' % (key), BLUE)
	print largeHex2Bin(key), len(largeHex2Bin(key))

	key = largeHex2Bin(key)
	cipherBlock = largeHex2Bin(cipherBlock)

	block = controlBlock('dec', '## invShiftRows3', '## invSubBytes3', cipherBlock)
	block = controlBlock('dec', '## invSubBytes3', '## addRoundKey3', block)
	block = controlBlock('dec', '## addRoundKey3', '## invMixColumns3', block, largeHex2Bin('b692cf0b643dbdf1be9bc5006830b3fe'))
	block = controlBlock('dec', '## invMixColumns3', '## invShiftRows2', block)
	block = controlBlock('dec', '## invShiftRows2', '## invSubBytes2', block)
	block = controlBlock('dec', '## invSubBytes2', '## addRoundKey2', block)
	block = controlBlock('dec', '## addRoundKey2', '## invMixColumns2', block, largeHex2Bin('d6aa74fdd2af72fadaa678f1d6ab76fe'))
	block = controlBlock('dec', '## invMixColumns2', '## invShiftRows1', block)
	block = controlBlock('dec', '## invShiftRows1', '## invSubBytes1', block)
	block = controlBlock('dec', '## invSubBytes1', '## addRoundKey1', block)
	block = controlBlock('dec', '## addRoundKey1', '## invMixColumns1', block, key)
	block = controlBlock('dec', '## invMixColumns1', '## invShiftRows0', block)
	block = controlBlock('dec', '## invShiftRows0', '## invSubBytes0', block)
	block = controlBlock('dec', '## invSubBytes0', '## addRoundKey0', block)
	block = controlBlock('dec', '## addRoundKey0', '## end', block, key)
	print('%s (FIPS result)' % clearBlock)
	return block


def generateDecFullFiles():
	printColor('## Deciphering process', YELLOW)
	createAESFiles('dec')
	addRoundKey(10, 'dec')
	writeRoundDec(9, invSubBytes(), invShiftRows())
	addRoundKey(9, 'dec')
	writeInvMixColumns(9)
	writeRoundDec(8, invSubBytes(), invShiftRows())
	addRoundKey(8, 'dec')
	writeInvMixColumns(8)
	writeRoundDec(7, invSubBytes(), invShiftRows())
	addRoundKey(7, 'dec')
	writeInvMixColumns(7)
	writeRoundDec(6, invSubBytes(), invShiftRows())
	addRoundKey(6, 'dec')
	writeInvMixColumns(6)
	writeRoundDec(5, invSubBytes(), invShiftRows())
	addRoundKey(5, 'dec')
	writeInvMixColumns(5)
	writeRoundDec(4, invSubBytes(), invShiftRows())
	addRoundKey(4, 'dec')
	writeInvMixColumns(4)
	writeRoundDec(3, invSubBytes(), invShiftRows())
	addRoundKey(3, 'dec')
	writeInvMixColumns(3)
	writeRoundDec(2, invSubBytes(), invShiftRows())
	addRoundKey(2, 'dec')
	writeInvMixColumns(2)
	writeRoundDec(1, invSubBytes(), invShiftRows())
	addRoundKey(1, 'dec')
	writeInvMixColumns(1)
	writeRoundDec(0, invSubBytes(), invShiftRows())
	addRoundKey(0, 'dec')
#	print currentStep, len(currentStep)
#	bitToLatex(currentStep[127])
	writeEndFlag('dec')
	printColor('## Files generated', YELLOW)


def controlDecFullFiles():
	cipherBlock = '69c4e0d86a7b0430d8cdb78070b4c55a'
	key = '000102030405060708090a0b0c0d0e0f'
	clearBlock = '00112233445566778899aabbccddeeff'

	printColor('## Cipher block %s' % (cipherBlock), BLUE)
	print largeHex2Bin(cipherBlock), len(largeHex2Bin(cipherBlock))
	printColor('## Key block %s' % (key), BLUE)
	print largeHex2Bin(key), len(largeHex2Bin(key))

	key = largeHex2Bin(key)
	cipherBlock = largeHex2Bin(cipherBlock)

	block = controlBlock('dec', '## addRoundKey10', '## Round9', cipherBlock, largeHex2Bin('549932d1f08557681093ed9cbe2c974e'))
	block = controlBlock('dec', '## Round9', '## addRoundKey9', block)
	block = controlBlock('dec', '## addRoundKey9', '## invMixColumns9', block, largeHex2Bin('47438735a41c65b9e016baf4aebf7ad2'))
	block = controlBlock('dec', '## invMixColumns9', '## Round8', block)
	block = controlBlock('dec', '## Round8', '## addRoundKey8', block)
	block = controlBlock('dec', '## addRoundKey8', '## invMixColumns8', block, largeHex2Bin('14f9701ae35fe28c440adf4d4ea9c026'))
	block = controlBlock('dec', '## invMixColumns8', '## Round7', block)
	block = controlBlock('dec', '## Round7', '## addRoundKey7', block)
	block = controlBlock('dec', '## addRoundKey7', '## invMixColumns7', block, largeHex2Bin('5e390f7df7a69296a7553dc10aa31f6b'))
	block = controlBlock('dec', '## invMixColumns7', '## Round6', block)
	block = controlBlock('dec', '## Round6', '## addRoundKey6', block)
	block = controlBlock('dec', '## addRoundKey6', '## invMixColumns6', block, largeHex2Bin('3caaa3e8a99f9deb50f3af57adf622aa'))
	block = controlBlock('dec', '## invMixColumns6', '## Round5', block)
	block = controlBlock('dec', '## Round5', '## addRoundKey5', block)
	block = controlBlock('dec', '## addRoundKey5', '## invMixColumns5', block, largeHex2Bin('47f7f7bc95353e03f96c32bcfd058dfd'))
	block = controlBlock('dec', '## invMixColumns5', '## Round4', block)
	block = controlBlock('dec', '## Round4', '## addRoundKey4', block)
	block = controlBlock('dec', '## addRoundKey4', '## invMixColumns4', block, largeHex2Bin('b6ff744ed2c2c9bf6c590cbf0469bf41'))
	block = controlBlock('dec', '## invMixColumns4', '## Round3', block)
	block = controlBlock('dec', '## Round3', '## addRoundKey3', block)
	block = controlBlock('dec', '## addRoundKey3', '## invMixColumns3', block, largeHex2Bin('b692cf0b643dbdf1be9bc5006830b3fe'))
	block = controlBlock('dec', '## invMixColumns3', '## Round2', block)
	block = controlBlock('dec', '## Round2', '## addRoundKey2', block)
	block = controlBlock('dec', '## addRoundKey2', '## invMixColumns2', block, largeHex2Bin('d6aa74fdd2af72fadaa678f1d6ab76fe'))
	block = controlBlock('dec', '## invMixColumns2', '## Round1', block)
	block = controlBlock('dec', '## Round1', '## addRoundKey1', block)
	block = controlBlock('dec', '## addRoundKey1', '## invMixColumns1', block, key)
	block = controlBlock('dec', '## invMixColumns1', '## Round0', block)
	block = controlBlock('dec', '## Round0', '## addRoundKey0', block)
	block = controlBlock('dec', '## addRoundKey0', '## end', block, key)
	print('%s (FIPS result)' % clearBlock)
