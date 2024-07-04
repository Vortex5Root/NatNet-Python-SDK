import socket
import struct
import logging

logging.basicConfig(level=logging.DEBUG)

logging.debug("Starting Multicast Receiver")
# Multicast Information
MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
IS_ALL_GROUPS = False
logging.debug("Multicast Group: %s", MCAST_GRP)
logging.debug("Multicast Port: %s", MCAST_PORT)
logging.debug("All Groups: %s", IS_ALL_GROUPS)

logging.debug("Creating Socket")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # Create UDP socket
logging.debug("Setting Socket Options and Binding to Port %s", MCAST_PORT)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow multiple copies of this program on one machine

if IS_ALL_GROUPS:
    sock.bind(('', MCAST_PORT)) # Binds to all interfaces
else:
    sock.bind((MCAST_GRP, MCAST_PORT)) # Binds to a specific multicast group

    logging.debug("Joining Multicast Group")
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY) # Request to join multicast group

    logging.debug("Setting Socket Options")
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq) # Request to join multicast group

while True:
    logging.debug("Receiving Data")
    data, address = sock.recvfrom(1024)
    print(address,data)
    sock.sendto(b'Hello World', address) # Send data to the multicast group