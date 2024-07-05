import socket

from typing import Generator, Tuple, Bytes

import logging

class MulticastServer:

    def __init__(self,
        multicast_port : int,
        multicast_group : str = None,
        
    ):
