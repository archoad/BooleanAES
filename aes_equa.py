#! /usr/bin/env python
# -*- coding: utf-8 -*-


from libmain import *
from libsubbytes import *
from libshiftrows import *
from libmixcolumns import *
from libkeyexpansion import *
from libkeyexpansion import *
from aes_equa_enc import *
from aes_equa_dec import *


def testAESdirectory(val):
	d = os.path.dirname(directory)
	if os.path.exists(d):
		os.rmdir(directory)



def encryptionProcess(step=True):
	if (step):
		generateEncStepsFiles()
		controlEncStepsFiles()
	else:
		generateEncFullFiles()
		controlEncFullFiles()


def decryptionProcess(step=True):
	if (step):
		generateDecStepsFiles()
		controlDecStepsFiles()
	else:
		generateDecFullFiles()
		controlDecFullFiles()







if __name__ == "__main__":
	#testKeyExpansion()
