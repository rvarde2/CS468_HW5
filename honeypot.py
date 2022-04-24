#!/usr/bin/env python
import io
import socket
import sys,getopt
from os.path import exists
import threading
import paramiko

host_key = '''
-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
'''

USERS = {}
ATTEPTS_BEFORE_SUCCESS = 5

class Server(paramiko.ServerInterface):
	def __init__(self):
		self.event = threading.Event()

	def check_channel_request(self, kind, chanid):
		if kind == 'session':
			return paramiko.OPEN_SUCCEEDED
		return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

	def check_channel_shell_request(self, channel):
		self.event.set()
		return True

	def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
		return True

	def get_allowed_auths(self, username):
		# There are three possible returns corresponding to authentication method for user
		# password, publickey, none
		# Enforcing Password Authentication method for all users
		return 'password'

	# Authentication by password
	def check_auth_password(self, username, password):
		global USERS
		global ATTEPTS_BEFORE_SUCCESS
		if(username in USERS):
			USERS[username] = USERS[username] + 1
			print(username,' attempt no. ',USERS[username])
			if(USERS[username] >= ATTEPTS_BEFORE_SUCCESS):
				return paramiko.AUTH_SUCCESSFUL
		else:	
			USERS[username] = 1
			print(username,' attempt no. ',USERS[username])
			return paramiko.AUTH_FAILED

	# Authentication by Key
	def check_auth_publickey(self, username, key):
		return paramiko.AUTH_FAILED

	# No Authentication
	def check_auth_none(self,username):
		return paramiko.AUTH_FAILED

	# Command argument provided by ssh client
	def check_channel_exec_request(self, channel, command):
		print ('Command:',command)
		self.event.set()
		return True

def main(argv):
	port = 2222
	global host_key
	try:
		opts, args = getopt.getopt(argv,"p:")
	except getopt.GetoptError:
		print('Unexpected Argument')
		return 

	for opt, arg in opts:
		if (opt == '-p'):
			port = int(arg)
			if( (port < 1) and (port > 65535)):
				print('Port should be within range 1 to 65535')
				return

	rsa_key = paramiko.RSAKey.from_private_key(io.StringIO(host_key))
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	try:
		sock.bind(('', port))
	except Exception as e:
		print('Issue socket binding')
		return

	sock.listen(100)

	while True:
		try:
			# Accept TCP Connection from Client
			client, addr = sock.accept()
			print('Connection from request from ',addr[0])
			transport = paramiko.Transport(client)
			transport.add_server_key(rsa_key)
			transport.local_version = "SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.3"
		except Exception as e:
			print(e)
			raise Exception('Issue in acceptng client')

		try:
			# Start SSH Server for incoming Client
			server = Server()
			transport.start_server(server=server)
		except paramiko.SSHException:
			raise('SSH Negotiation Failed')

		# Authenticate Client
		chan = transport.accept(20)
		if chan is None:
			# Too many incorrect password attempts
			print("Failed to acquire the Channel")
			continue

		server.event.wait(10)

		if not server.event.is_set():
			raise Exception("Shell not request")

		chan.send("Welcome to Jumanji!!!\r\n\r\n")


if __name__ == '__main__':
    main(sys.argv[1:])