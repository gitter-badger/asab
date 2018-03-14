import logging
import asab

from .protocol import HTTPServerProtocol

#

L = logging.getLogger(__name__)

#

class ServiceHTTPServer(asab.StreamSocketServerService):


	async def initialize(self, app):
		#TODO: Multiple http server support
		host = asab.Config.get('http', 'host')
		port = asab.Config.getint('http', 'port')

		L.debug("Starting HTTP server on {} {} ...".format(host, port))
		await self.create_server(app, HTTPServerProtocol, [(host, port)])
