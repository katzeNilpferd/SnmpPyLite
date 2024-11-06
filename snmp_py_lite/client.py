from transport import Transport
from message import SNMPMessage
from format import SNMPFormat


class SNMPClient:
    def __init__(self, ip: str, community='public', version=0, port=161, timeout=1, retries=5):
        self.ip = ip
        self.community = community
        self.version = version
        self.port = port
        self.timeout = timeout
        self.retries = retries
        self.transport = Transport(ip, port, timeout, retries)
        self.message = SNMPMessage(version, community)
        self.format = SNMPFormat()
        
    def get(self, oid):
        return self._send_request('get', oid)
    
    def get_next(self, oid):
        return self._send_request('get_next', oid)
    
    def get_bulk(self, oid):
        return self._send_request('get_bulk', oid)

    def get_walk(self, oid):
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

    def set(self, oid, value, value_type):
        return self._send_request('set', oid, value_type=value_type, value=value)
    
    def _send_request(self, request_type, oid, **kwargs):
        status = 'ok'
        raw_data = list()

        try:
            if request_type == 'get':
                request = self.message.create_get_request(oid)
            elif request_type == 'get_next':
                request = self.message.create_get_next_request(oid)
            elif request_type == 'get_bulk':
                request = self.message.create_get_bulk_request(oid)
            elif request_type == 'set':
                value = kwargs.get('value')
                value_type = kwargs.get('value_type')
                request = self.message.create_set_request(oid, value_type, value)
            else:
                raise ValueError("invalid request type")
                
            response = self.transport.send(request)
            raw_data = self.message.parse_response(response)
        except Exception as e:
            status = str(e)

        return self.format.formar_response(self.ip, status, raw_data)
