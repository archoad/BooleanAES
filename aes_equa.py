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








if __name__ == "__main__":
	#testKeyExpansion()

	#generateEncStepsFiles()
	#controlEncStepsFiles()

	#generateEncFullFiles()
	#controlEncFullFiles()

	#generateDecStepsFiles()
	#controlDecStepsFiles()

	generateDecFullFiles()
	controlDecFullFiles()
