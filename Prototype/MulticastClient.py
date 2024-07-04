from threading import Thread
from Multicast_Client import MulticastClient

class NatClient:
    def __init__(self,
        multi_cast_ip : str,
        multi_cast_port : int,
        server_ip : str = None,
    ) -> None:
        self.multi_cast_ip = multi_cast_ip
        self.server_ip = server_ip
        self.server_port = multi_cast_port
        self.client = MulticastClient(multicast_port=self.server_port, multicast_group=self.multi_cast_ip, interface_ip=self.server_ip, multicast_ttl=2)
        Thread(target=self.receive).start()
        self.client.send(b'Hello World')
        
    def receive(self):
        for data in self.client.connect():
            # Process Data
            print(data)
            pass
    
NatClient(multi_cast_ip='224.1.1.1', multi_cast_port=5007)