from httptools import parse_url

class Request(object):


	def __init__(self, url_bytes, headers, version, method,transport):
		self._parsed_url = parse_url(url_bytes)

		self.headers = headers
		self.version = version
		self.method = method
		self.transport = transport

		# Init but do not inhale
		self.body = []
		self.parsed_json = None
		self.parsed_form = None
		self.parsed_files = None
		self.parsed_args = None
		self.uri_template = None
		self._cookies = None
		self.stream = None


	def __repr__(self):
		if self.method is None or not self.path:
			return '<{0}>'.format(self.__class__.__name__)

		return '<{0}: {1} {2}>'.format(self.__class__.__name__, self.method, self.path)
