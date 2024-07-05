import socket

import logging

class Socket_Clinet:

    local_ip_address  : str = "127.0.0.1"
    server_ip_address : str = "127.0.0.1"
    
    multicast_address : str = "239.255.42.99"

    command_port : int = 1510
    data_port : int = 1511

    use_multicast : bool = True

    def __init__(self,logging_level : int = logging.DEBUG) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging_level)
        self.logger.info("Starting Multicast Client")


    def create_sender_socket(self):
        connection_sender = None
        if self.use_multicast:
            # Create a multicast socket
            connection_sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
            # allow multiple clients on same machine to use multicast group address/port
            connection_sender.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                connection_sender.bind(('', 0))
            except socket.error as msg: # Catch socket errors
                self.logger.error("ERROR: command socket error occurred:\n" + str(msg))
                connection_sender = None
            # set to broadcast mode
            connection_sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            # set timeout to allow for keep alive messages
            connection_sender.settimeout(2.0)
        else:
            # Create a unicast socket
            connection_sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
            try:
                connection_sender.bind((self.local_ip_address, 0))
            except socket.error as msg:
                self.logger.error("ERROR: command socket error occurred:\n" + str(msg))
                connection_sender = None
            except Exception as e:
                self.logger.error("ERROR:\n" + str(e))
                connection_sender = None
            connection_sender.settimeout(2.0)
            connection_sender.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow multiple copies of this program on one machine
        return connection_sender   

    def create_receiver_socket(self,port):
        connection_receiver = None
        if self.use_multicast:
            # Create a multicast socket
            connection_receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0) # UDP
            connection_receiver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow multiple copies of this program on one machine
            connection_receiver.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(self.multicast_address) + socket.inet_aton(self.local_ip_address)) # Request to join multicast group
            try:
                connection_receiver.bind((self.local_ip_address, port))
            except socket.error as msg:
                self.logger.error("ERROR: data socket error occurred:\n" + str(msg))
                connection_receiver = None
        else:
            connection_receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            try:
                connection_receiver.bind((self.local_ip_address, 0))
            except socket.error as msg:
                self.logger.error("ERROR: data socket error occurred:\n" + str(msg))
                connection_receiver = None
            except Exception as e:
                self.logger.error("ERROR:\n" + str(e))
                connection_receiver = None

            # set timeout to allow for keep alive messages
            connection_receiver.settimeout(2.0)
            connection_receiver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return connection_receiver