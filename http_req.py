
class HTTPRequest:
	def __init__(self, data):
		self.method = None
		self.uri = None
		self.http_version = "1.1" #default to HTTP/1.1 if request doesn't provide one

		self.parse(data)

	def parse(self, data):
		lines = data.split(b"\r\n")
		request_line = lines[0]
		words = request_line.split(b" ")
		self.method = words[0].decode()

		if len(words) > 1:
			# in case browser don't send uri
			self.uri = words[1].decode()

		if len(words) > 2:
			self.http_version = words[2].decode()
			
		print(words[0:3])
