#!/usr/bin/env python
import socket
import sys,getopt
from os.path import exists
import threading
import paramiko

port = 1234
mode = 'password'
host_key = ''


class Server(paramiko.ServerInterface):
    def __init__(self):
        print('INIT')
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        print('CHAN REQ')
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_shell_request(self, channel):
        print('SHELL REQ')
        self.event.set()
        return True

    def check_channel_pty_request(
        self, channel, term, width, height, pixelwidth, pixelheight, modes
    ):
        print('PTY REQ')
        return True

    def get_allowed_auths(self, username):
        global mode
        print('ALLOWED AUTH')
        # Enforcing same Authentication method for all users
        # For variations populate dictionary with mapping of username to mode
        if(mode == 'key'):
            return 'publickey'
        elif(mode == 'password'):
            return 'password'
        return 'none'

    # Authentication by password
    def check_auth_password(self, username, password):
        print('Check_auth_password', username,password)
        if(mode == 'password'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    # Authentication by Key
    def check_auth_publickey(self, username, key):
        print('Check Auth Public Key:',username,key)
        if(mode == 'key'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    # No Authentication
    def check_auth_none(self,username):
        print('Check Auth None')
        if(mode == 'none'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    # Command argument provided by ssh client
    def check_channel_exec_request(self, channel, command):
        print ('Command:',command)
        self.event.set()
        return True

    


def main(argv):
    global port
    global mode
    global host_key
    key = ''
    try:
        opts, args = getopt.getopt(argv,"p:m:k:")
    except getopt.GetoptError:
        print('Unexpected Argument')
        return 

    for opt, arg in opts:
        if (opt == '-p'):
            port = int(arg)
            if( (port < 1) and (port > 65535)):
                print('Port should be within range 1 to 65535')
                return
        
        elif (opt == '-m'):
            mode = arg
            if(mode!='password' and mode!='key' and mode!='none'):
                print('Mode could be either password, key or none')
                return

        elif (opt == '-k'):
            key = arg
            if(not exists(key)):
                print('Key File Does not exists')
                return
            host_key = paramiko.RSAKey(filename=key)
            print(host_key)

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
            #if(mode=='key'):
            transport.add_server_key(host_key)
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
            raise Exception("Failed to acquire the Channel")

        server.event.wait(10)

        if not server.event.is_set():
            raise Exception("Shell not request")

        chan.send("Welcome to Jumanji!!!\r\n\r\n")


if __name__ == '__main__':
    main(sys.argv[1:])