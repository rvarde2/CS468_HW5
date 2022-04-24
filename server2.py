#!/usr/bin/env python
import logging
import socket
import sys
import threading

import paramiko

logging.basicConfig()
logger = logging.getLogger()

if len(sys.argv) != 2:
    print ("Need private host RSA key as argument.")
    sys.exit(1)

host_key = paramiko.RSAKey(filename=sys.argv[1])


class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_publickey(self, username, key):
        print('Check Auth Public Key:',username,key)
        return paramiko.AUTH_SUCCESSFUL

    def get_allowed_auths(self, username):
        print('Get Allowed Auths:',username)
        return 'publickey'

    def check_channel_exec_request(self, channel, command):
        # This is the command we need to parse
        print ('Command:',command)
        self.event.set()
        return True

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(
        self, channel, term, width, height, pixelwidth, pixelheight, modes
    ):
        return True



def listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 1234))

    sock.listen(100)
    print('Ready to accept connection')
    client, addr = sock.accept()
    print('Connection Accepted')
    t = paramiko.Transport(client)
    t.set_gss_host(socket.getfqdn(""))
    t.load_server_moduli()
    t.add_server_key(host_key)
    server = Server()
    print('Starting Server...')
    t.start_server(server=server)
    print("Before Wait")
    # Wait 30 seconds for a command
    server.event.wait(30)
    print("After Wait")
    t.close()


while True:
    try:
        listener()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as exc:
        logger.error(exc)