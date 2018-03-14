import asyncio
import logging
import traceback
import httptools
import httptools.parser.errors
import asab

#from .request import Request
from .cidict import CIDict

#

L = logging.getLogger(__name__)

#

class HTTPServerProtocol(asyncio.Protocol):


	def __init__(self):
		
		self.transport = None
		self.parser = None

		self.request_class = Request
		self.request = None

		self.url = None
		self.headers = None


		self._header_fragment = b''


	def connection_made(self, transport):
		peername = transport.get_extra_info('peername')
		L.debug('Connection from {} -> {}'.format(peername, self))
		self.transport = transport


	def data_received(self, data):
		# Check for the request itself getting too large and exceeding memory limits
		# self._total_request_size += len(data)
		# if self._total_request_size > self.request_max_size:
		# 	exception = PayloadTooLarge('Payload Too Large')
		# 	self.write_error(exception)

		# Create parser if this is the first time we're receiving data
		if self.parser is None:
			assert self.request is None
			self.headers = []
			self.parser = httptools.HttpRequestParser(self)

		#TODO: Metrics requests count
		#self.state['requests_count'] = self.state['requests_count'] + 1

		# Parse request chunk or close connection
		try:
			self.parser.feed_data(data)
		except httptools.parser.errors.HttpParserError:
			RuntimeError("Bad Request")
			#TODO: write_error
			#message = 'Bad Request'
			#if self._debug:
			#	message += '\n' + traceback.format_exc()
			#exception = RuntimeError(message)
			#self.write_error(exception)


	# HttpRequestParser

	def on_message_begin(self):
		print("on_message_begin")


	def on_url(self, url: bytes):
		if self.url is None:
			self.url = url
		else:
			self.url += url


	def on_header(self, name: bytes, value: bytes):
		self._header_fragment += name

		if value is not None:
			if self._header_fragment == b'Content-Length' and int(value) > self.request_max_size:
				#TODO: write_error
				#exception = PayloadTooLarge('Payload Too Large')
				#self.write_error(exception)
				raise RuntimeError('Payload Too Large')
			try:
				value = value.decode()
			except UnicodeDecodeError:
				value = value.decode('latin_1')
			self.headers.append((self._header_fragment.decode().lower(), value))
			self._header_fragment = b''


	def on_headers_complete(self):
		try:
			self.request = self.request_class(
				url_bytes=self.url,
				headers=CIDict(self.headers),
				version=self.parser.get_http_version(),
				method=self.parser.get_method().decode(),
				transport=self.transport
			)
		except:
			#TODO: Handle this ...
			L.exception("on_headers_complete")

		print("BB", self.request)


	def on_body(self, body: bytes):
		print("on_body", body)

	def on_message_complete(self):
		print("on_message_complete")

	def on_chunk_header(self):
		print("on_chunk_header")

	def on_chunk_complete(self):
		print("on_chunk_complete")
