

from libmain import *
from libsubbytes import *
from libshiftrows import *
from libmixcolumns import *
from libkeyexpansion import *


def generateRoundEncEqua(equaSB, equaSR, equaMC):
	resultSR = []
	resultMC = []
	for i in range(blockSize):
		equaSR[i] = equaSR[i].split('_')
		resultSR.append(equaSB[int(equaSR[i][1])])

	for i in range(blockSize):
		tmp = ''
		for monomial in equaMC[i].split('+'):
			tmp += resultSR[int(monomial.split('_')[1])]
			tmp += '+'
		resultMC.append(tmp.rstrip('+'))
	return resultMC


def generateRoundEnc(equaSB, equaSR, equaMC):
	resultSR = []
	resultMC = []
	for i in range(blockSize):
		equaSR[i] = equaSR[i].split('_')
		resultSR.append(equaSB[int(equaSR[i][1])])

	for i in range(blockSize):
		tmp = ''
		for monomial in equaMC[i].split('+'):
			tmp += resultSR[int(monomial.split('_')[1])]
			tmp += '+'
		resultMC.append(tmp.rstrip('+'))
	binMon = generateBinaryMonomes(resultMC)
	return binMon


def writeSubBytes(numRound):
	printColor('## SubBytes%s' % numRound, GREEN)
	equa = subBytes()
	binMon = generateBinaryMonomes(equa)
	for i in range(blockSize):
		f = openFile(fileNameEnc+'%s.txt' % intToThreeChar(i))
		f.write('## subBytes%s\n' % numRound)
		f.write(binMon[i])
		closeFile(f)
	return equa


def writeShiftRows(numRound):
	printColor('## ShiftRows%s' % numRound, GREEN)
	equa = shiftRows()
	binMon = generateBinaryMonomes(equa)
	for i in range(blockSize):
		f = openFile(fileNameEnc+'%s.txt' % intToThreeChar(i))
		f.write('## shiftRows%s\n' % numRound)
		f.write(binMon[i])
		closeFile(f)
	return equa


def writeMixColumns(numRound):
	printColor('## MixColumns%s' % numRound, GREEN)
	equa = mixColumns()
	binMon = generateBinaryMonomes(equa)
	for i in range(blockSize):
		f = openFile(fileNameEnc+'%s.txt' % intToThreeChar(i))
		f.write('## mixColumns%s\n' % numRound)
		f.write(binMon[i])
		closeFile(f)
	return equa


def writeRoundEnc(numRound, equaSB, equaSR, equaMC):
	printColor('## Round%s' % numRound, GREEN)
	resultSR = []
	resultMC = []
	for i in range(blockSize):
		equaSR[i] = equaSR[i].split('_')
		resultSR.append(equaSB[int(equaSR[i][1])])

	for i in range(blockSize):
		tmp = ''
		for monomial in equaMC[i].split('+'):
			tmp += resultSR[int(monomial.split('_')[1])]
			tmp += '+'
		resultMC.append(tmp.rstrip('+'))
	binMon = generateBinaryMonomes(resultMC)

	for i in range(blockSize):
		f = openFile(fileNameEnc+'%s.txt' % intToThreeChar(i))
		f.write('## Round%s\n' % numRound)
		f.write(binMon[i])
		closeFile(f)
	return resultMC


def writeFinalRoundEnc(numRound, equaSB, equaSR):
	printColor('## Round%s' % numRound, GREEN)
	resultSR = []
	for i in range(blockSize):
		equaSR[i] = equaSR[i].split('_')
		resultSR.append(equaSB[int(equaSR[i][1])])
	binMon = generateBinaryMonomes(resultSR)

	for i in range(blockSize):
		f = openFile(fileNameEnc+'%s.txt' % intToThreeChar(i))
		f.write('## Round%s\n' % numRound)
		f.write(binMon[i])
		closeFile(f)
	return resultSR


def generateEncStepsFiles():
	createAESFiles('enc')
	addRoundKey(0, 'enc')
	writeSubBytes(0)
	writeShiftRows(0)
	writeMixColumns(0)
	addRoundKey(1, 'enc')
	writeSubBytes(1)
	writeShiftRows(1)
	writeMixColumns(1)
	addRoundKey(2, 'enc')
	writeSubBytes(2)
	writeShiftRows(2)
	writeMixColumns(2)
	writeEndFlag('enc')
#	print(currentStep, len(currentStep))
#	bitToLatex(currentStep[127])
	printColor('## Files generated', RED)


def controlEncStepsFiles():
	clearBlock = '00112233445566778899aabbccddeeff'
	key = '000102030405060708090a0b0c0d0e0f'
	fipsMixColumns2 = '4c9c1e66f771f0762c3f868e534df256'

	printColor('## Clear block %s' % (clearBlock), BLUE)
	print(largeHex2Bin(clearBlock), len(largeHex2Bin(clearBlock)))
	printColor('## Key block %s' % (key), BLUE)
	print(largeHex2Bin(key), len(largeHex2Bin(key)))

	key = largeHex2Bin(key)
	clearBlock = largeHex2Bin(clearBlock)

	block = controlBlock('enc', '## addRoundKey0', '## subBytes0', clearBlock, key)
	block = controlBlock('enc', '## subBytes0', '## shiftRows0', block)
	block = controlBlock('enc', '## shiftRows0', '## mixColumns0', block)
	block = controlBlock('enc', '## mixColumns0', '## addRoundKey1', block)
	block = controlBlock('enc', '## addRoundKey1', '## subBytes1', block, key)
	block = controlBlock('enc', '## subBytes1', '## shiftRows1', block)
	block = controlBlock('enc', '## shiftRows1', '## mixColumns1', block)
	block = controlBlock('enc', '## mixColumns1', '## addRoundKey2', block)
	block = controlBlock('enc', '## addRoundKey2', '## subBytes2', block, largeHex2Bin('d6aa74fdd2af72fadaa678f1d6ab76fe'))
	block = controlBlock('enc', '## subBytes2', '## shiftRows2', block)
	block = controlBlock('enc', '## shiftRows2', '## mixColumns2', block)
	block = controlBlock('enc', '## mixColumns2', '## end', block)
	print('%s (FIPS result)' % fipsMixColumns2)


def generateEncFullFiles():
	printColor('## Ciphering process', YELLOW)
	createAESFiles('enc')
	addRoundKey(0, 'enc')
	writeRoundEnc(0, subBytes(), shiftRows(), mixColumns())
	addRoundKey(1, 'enc')
	writeRoundEnc(1, subBytes(), shiftRows(), mixColumns())
	addRoundKey(2, 'enc')
	writeRoundEnc(2, subBytes(), shiftRows(), mixColumns())
	addRoundKey(3, 'enc')
	writeRoundEnc(3, subBytes(), shiftRows(), mixColumns())
	addRoundKey(4, 'enc')
	writeRoundEnc(4, subBytes(), shiftRows(), mixColumns())
	addRoundKey(5, 'enc')
	writeRoundEnc(5, subBytes(), shiftRows(), mixColumns())
	addRoundKey(6, 'enc')
	writeRoundEnc(6, subBytes(), shiftRows(), mixColumns())
	addRoundKey(7, 'enc')
	writeRoundEnc(7, subBytes(), shiftRows(), mixColumns())
	addRoundKey(8, 'enc')
	writeRoundEnc(8, subBytes(), shiftRows(), mixColumns())
	addRoundKey(9, 'enc')
	writeFinalRoundEnc(9, subBytes(), shiftRows())
	addRoundKey(10, 'enc')
	writeEndFlag('enc')
#	print(currentStep, len(currentStep))
#	bitToLatex(currentStep[127])
	printColor('## Files generated', YELLOW)


def controlEncFullFiles():
	clearBlock = '00112233445566778899aabbccddeeff'
	key = '000102030405060708090a0b0c0d0e0f'
	cipherBlock = '69c4e0d86a7b0430d8cdb78070b4c55a'

	printColor('## Clear block %s' % (clearBlock), BLUE)
	print(largeHex2Bin(clearBlock), len(largeHex2Bin(clearBlock)))
	printColor('## Key block %s' % (key), BLUE)
	print(largeHex2Bin(key), len(largeHex2Bin(key)))

	key = largeHex2Bin(key)
	clearBlock = largeHex2Bin(clearBlock)

	block = controlBlock('enc', '## addRoundKey0', '## Round0', clearBlock, key)
	block = controlBlock('enc', '## Round0', '## addRoundKey1', block)
	block = controlBlock('enc', '## addRoundKey1', '## Round1', block, key)
	block = controlBlock('enc', '## Round1', '## addRoundKey2', block)
	block = controlBlock('enc', '## addRoundKey2', '## Round2', block, largeHex2Bin('d6aa74fdd2af72fadaa678f1d6ab76fe'))
	block = controlBlock('enc', '## Round2', '## addRoundKey3', block)
	block = controlBlock('enc', '## addRoundKey3', '## Round3', block, largeHex2Bin('b692cf0b643dbdf1be9bc5006830b3fe'))
	block = controlBlock('enc', '## Round3', '## addRoundKey4', block)
	block = controlBlock('enc', '## addRoundKey4', '## Round4', block, largeHex2Bin('b6ff744ed2c2c9bf6c590cbf0469bf41'))
	block = controlBlock('enc', '## Round4', '## addRoundKey5', block)
	block = controlBlock('enc', '## addRoundKey5', '## Round5', block, largeHex2Bin('47f7f7bc95353e03f96c32bcfd058dfd'))
	block = controlBlock('enc', '## Round5', '## addRoundKey6', block)
	block = controlBlock('enc', '## addRoundKey6', '## Round6', block, largeHex2Bin('3caaa3e8a99f9deb50f3af57adf622aa'))
	block = controlBlock('enc', '## Round6', '## addRoundKey7', block)
	block = controlBlock('enc', '## addRoundKey7', '## Round7', block, largeHex2Bin('5e390f7df7a69296a7553dc10aa31f6b'))
	block = controlBlock('enc', '## Round7', '## addRoundKey8', block)
	block = controlBlock('enc', '## addRoundKey8', '## Round8', block, largeHex2Bin('14f9701ae35fe28c440adf4d4ea9c026'))
	block = controlBlock('enc', '## Round8', '## addRoundKey9', block)
	block = controlBlock('enc', '## addRoundKey9', '## Round9', block, largeHex2Bin('47438735a41c65b9e016baf4aebf7ad2'))
	block = controlBlock('enc', '## Round9', '## addRoundKey10', block)
	block = controlBlock('enc', '## addRoundKey10', '## end', block, largeHex2Bin('549932d1f08557681093ed9cbe2c974e'))
	print('%s (FIPS result)' % (cipherBlock))
