from .transport import Transport
from .message import SNMPMessage
from .format import SNMPFormat
from typing import Generator


class SNMPClient:
    def __init__(self, ip: str, community='public', version=0, port=161, timeout=1, retries=3):
        self.ip = ip
        self.community = community
        self.version = version
        self.port = port
        self.timeout = timeout
        self.retries = retries
        self.transport = Transport(ip, port, timeout, retries)
        self.message = SNMPMessage(version, community)
        self.format = SNMPFormat()
        
    def get(self, oid: str) -> dict:
        return self._send_request('get', oid)
    
    def get_next(self, oid: str) -> dict:
        return self._send_request('get_next', oid)
    
    def get_bulk(self, oid: str, non_repeaters=0, max_repetitions=10) -> dict:
        if self.version == 0:
            raise Exception('For the get_bulk operation, the specified version must be 2 or higher')
        
        return self._send_request('get_bulk', oid, non_repeaters, max_repetitions)

    def get_walk(self, oid: str) -> Generator[dict, None, None]:
        oid = SNMPFormat.format_oid(oid)
        current_oid = oid
        
        while True:
            response = self.get_next(current_oid)
            try:
                next_oid = list(response["data"].keys())[0]
                if not next_oid.startswith(oid):
                    break
                current_oid = next_oid
            except:
                break
            
            finally:
                yield response

    def set(self, oid: str, value_type: str, value: str | int) -> dict:
        return self._send_request('set', oid, value_type, value)
    
    def _send_request(self, request_type, oid, *args):
        oid = SNMPFormat.format_oid(oid)
        
        if request_type == 'get':
            request = self.message.create_get_request(oid)
            
        elif request_type == 'get_next':
            request = self.message.create_get_next_request(oid)
            
        elif request_type == 'get_bulk':
            non_repeaters = args[0]
            max_repetitions = args[1]
            request = self.message.create_get_bulk_request(oid, non_repeaters, max_repetitions)
            
        elif request_type == 'set':
            value_type = args[0]
            value = args[1]
            request = self.message.create_set_request(oid, value_type, value)
            
        else:
            raise ValueError("invalid request type")
        
        response = self.transport.send(request)
        raw_data = self.message.parse_response(response)
        return self.format.formar_response(self.ip, raw_data)
