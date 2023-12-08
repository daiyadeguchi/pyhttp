import socket

class TCPServer:

	def __init__(self, host='127.0.0.1', port=8888):
		self.host = host
		self.port = port

	def start(self):
		# AF_INET = address family for IPv4
		# SOCK_STREAM = TCP socket
		# SOCK_DGRAM = UDP socket
		# https://docs.python.org/3/library/socket.html#socket.AF_INET
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((self.host, self.port))
		# queue up as many as 5 connect requests
		s.listen(5)

		print("Listening at", s.getsockname())

		while True:
			conn, addr = s.accept()
			print("Connected by", addr)

			# read the first 1024 bytes of data
			data = conn.recv(1024)

			response = self.handle_request(data)

			# sent back the data to client
			conn.sendall(response)
			conn.close()

	def handle_request(self, data):
		"""
		Handles incoming data and returns a response
		Override this in subclass
		"""
		return data
