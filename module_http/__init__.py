import logging
import asab

from .service import ServiceHTTPServer

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

		self._service_http_server = ServiceHTTPServer(app)
		app.register_service("service_http_server", self._service_http_server)
