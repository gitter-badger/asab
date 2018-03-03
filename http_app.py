#!/usr/bin/env python3
import sys
import asab

###

class HttpApplication(asab.Application):

	def __init__(self):
		super().__init__()

###

if __name__ == '__main__':
	app = HttpApplication()

	from module_http import Module
	app.add_module(Module)

	ret = app.run()
	sys.exit(ret)
