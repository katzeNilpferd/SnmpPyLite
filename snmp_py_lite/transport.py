import socket


class Transport:
    def __init__(self, ip, port, timeout, retries):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.retries = retries

    def send(self, message):     
        for attempt in range(self.retries):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(self.timeout)
                sock.sendto(message, (self.ip, self.port))
                data, _ = sock.recvfrom(4096)
                return data
            
            except Exception as e:
                if attempt == self.retries - 1:
                    
                    if str(e) == 'timed out':
                        raise ValueError('Timed out')
                    else:
                        raise ValueError('Incorrect ip address')
                
            finally:
                sock.close()
