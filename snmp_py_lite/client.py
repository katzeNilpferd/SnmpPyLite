from transport import Transport
from message import SNMPMessage


class SNMPClient:
    def __init__(self, ip, community='public', version=0, port=161):
        self.ip = ip
        self.community = community
        self.version = version
        self.port = port
        self.transport = Transport(ip, port)
        self.message = SNMPMessage(version, community)
        
    def get(self, oid):
        request = self.message.create_get_request(oid)
        response = self.transport.send(request)
        return self.message.parse_response(response)
    
    def set(self, oid, value):
        # Формирует и отправляет SET-запрос
        pass
    
    def walk(self, oid):
        # Реализация SNMP WALK
        pass


if __name__ == '__main__':
    client = SNMPClient('192.168.45.158', community='public')
    response = client.get('1.3.6.1.2.1.1.1.0')  # OID для sysDescr
    print(f"Ответ SNMP: {response}")