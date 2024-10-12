import socket


class Transport:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def send(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.sendto(message, (self.ip, self.port))
            data, _ = sock.recvfrom(1024)
            return data
        
        finally:
            sock.close()
