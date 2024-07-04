import socket

from typing import Generator, Tuple

import logging

class MulticastClient:
    def __init__(self,
        multicast_port : int,
        multicast_group : str = None,
        multicast_ttl : int = None,
        interface_ip : str = None,
        logging_level : int = logging.DEBUG
    ) -> None:
        # Set up logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging_level)
        # Set up Multicast Client
        self.logger.debug("Starting Multicast Client")
        self.multicast_port = multicast_port
        self.multicast_group = multicast_group
        self.multicast_ttl = multicast_ttl
        self.interface_ip = interface_ip
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        # Log Multicast Information
        self.logger.debug("Multicast Port: %s", self.multicast_port)
        self.logger.debug("Multicast Group: %s", self.multicast_group)
        self.logger.debug("Multicast TTL: %s", self.multicast_ttl)
        self.logger.debug("Interface IP: %s", self.interface_ip)
        self.logger.debug("Creating Socket")
        self.connect()

    def connect(self) -> Generator:
        if self.interface_ip is not None and self.multicast_group is not None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            mreq = socket.inet_aton(self.multicast_group) + socket.inet_aton(self.interface_ip)
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, str(mreq))
            logging.debug("Joining Multicast Group")
        elif self.multicast_ttl is not None:
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, self.multicast_ttl)
        else:
            self.sock.bind(('', self.multicast_port))
        while 1:
            data = self.sock.recv(10240)
            self.logger.debug("Receiving Data", data)
            yield data

    def send(self, data : bytes) -> None:
        self.sock.sendto(data, (self.multicast_group, self.multicast_port))
