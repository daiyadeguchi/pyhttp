import os
from tcp import TCPServer
from http_req import HTTPRequest

class HTTPServer(TCPServer):
	headers = {
		'Server': 'CrudeServer',
		'Content-Type': 'text/html',
	}

	status_codes = {
		200: 'OK',
		404: 'Not Found',
		501: 'Not Implemented',
	}

	def handle_request(self, data):
		request = HTTPRequest(data)

		try:
			handler = getattr(self, 'handle_%s' % request.method)
		except AttributeError:
			handler = self.HTTP_501_handler

		response = handler(request)

		return response

	def handle_GET(self, request):
		uri = str(request.uri)
		filename = uri.strip('/')
		print(filename)
		if os.path.exists(filename):
			response_line = self.response_line(status_code=200)
			response_headers = self.response_headers()
			with open(filename, 'rb') as f:
				response_body = f.read()
		else:
			response_line = self.response_line(status_code=404)
			response_headers = self.response_headers()
			response_body = b"<h1>404 Not Found</h1>"

		blank_line = b"\r\n"

		return b"".join([response_line, response_headers, blank_line, response_body])

	def HTTP_501_handler(self, request):
		response_line = self.response_line(status_code=501)
		response_headers = self.response_headers()
		blank_line = b"\r\n"
		response_body = b"<h1>501 Not Implemented</h1>"
		return b"".join([response_line, response_headers, blank_line, response_body])

	def response_line(self, status_code):
		reason = self.status_codes[status_code]
		line = "HTTP/1.1 %s %s\r\n" % (status_code, reason)
		return line.encode() # encode because we want BYTES!

	def response_headers(self, extra_headers=None):
		"""
		Returns headers
		The 'extra_headers' can be a dict for sending
		extra headers for the current response
		"""
		headers_copy = self.headers.copy() # make a local copy of headers

		if extra_headers:
			headers_copy.update(extra_headers)

		headers = ""

		for h in headers_copy:
			headers += "%s: %s\r\n" % (h, headers_copy[h])

		return headers.encode() # BYTES!
