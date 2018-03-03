import logging
import asab

from .protocol import HTTPServerProtocol

#

L = logging.getLogger(__name__)

#

asab.Config.add_defaults(
	{
		'http': {
			'host': '127.0.0.1',
			'port': 8888,
		}
	}
)

#

class Module(asab.Module):

	def __init__(self, app):
		super().__init__(app)

		self.servers = []

		coro = app.Loop.create_server(HTTPServerProtocol, app.Config.get('http', 'host'), app.Config.getint('http', 'port'))
		server = app.Loop.run_until_complete(coro)
		self.servers.append(server)
