from .transport import Transport
from .message import SNMPMessage
from .format import SNMPFormat
from typing import Union, Generator
from .constants import *


class SNMPClient:
    """
    A client for interacting with SNMP agents using basic SNMP operations.

    This class provides methods to perform SNMP operations such as GET, GET-NEXT, GET-BULK, GET-WALK, and SET.
    It abstracts the details of SNMP message creation, transport handling, and response formatting.

    Attributes:
        ip (str): IP address of the SNMP agent.
        community (str): SNMP community string. Default is 'public'.
        version (str): SNMP version ('1' = SNMPv1, '2c' = SNMPv2c). Default is '1'.
        port (int): UDP port of the SNMP agent. Default is 161.
        timeout (int): Timeout for SNMP requests, in seconds. Default is 1.
        retries (int): Number of retries for SNMP requests. Default is 3.
        transport (Transport): Handles sending and receiving SNMP messages.
        message (SNMPMessage): Creates and parses SNMP messages.
        format (SNMPFormat): Validates and formats the SNMP responses.
    """

    def __init__(self, ip: str, community='public', version='1', port=161, timeout=1, retries=3):
        self.ip = ip
        self.community = community
        self.version = SNMP_VERSIONS[version]
        self.port = port
        self.timeout = timeout
        self.retries = retries
        
        self.transport = Transport(ip, port, timeout, retries)
        self.message = SNMPMessage(self.version, community)
        self.format = SNMPFormat()
        
    def get(self, oid: str) -> dict:
        """
        Performs an SNMP GET operation to retrieve the value of the specified OID.

        Args:
            oid (str): The OID to retrieve.

        Returns:
            dict: The formatted response containing the retrieved value.
        """
        return self._send_request('get', oid)
    
    def get_next(self, oid: str) -> dict:
        """
        Performs an SNMP GET-NEXT operation to retrieve the next OID and its value.

        Args:
            oid (str): The OID to start from.

        Returns:
            dict: The formatted response containing the next OID and its value.
        """
        return self._send_request('get_next', oid)
    
    def get_bulk(self, oid: str, non_repeaters=0, max_repetitions=10) -> dict:
        """
        Performs an SNMP GET-BULK operation to retrieve multiple OIDs in a single request.

        Args:
            oid (str): The starting OID for the bulk request.
            non_repeaters (int): Number of non-repeating variables. Default is 0.
            max_repetitions (int): Maximum number of repeating variables. Default is 10.

        Returns:
            dict: The formatted response containing the retrieved OIDs and their values.

        Raises:
            Exception: If the SNMP version is not 2c or higher.
        """
        if self.version == 0:
            raise Exception('For the get_bulk operation, the specified version must be 2c or higher')
        
        return self._send_request('get_bulk', oid, non_repeaters, max_repetitions)

    def get_walk(self, oid: str) -> Generator[dict, None, None]:
        """
        Performs an SNMP WALK operation, iteratively retrieving all OIDs in a subtree.

        Args:
            oid (str): The root OID for the walk.

        Yields:
            dict: Formatted responses for each OID in the subtree.
        """
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

    def set(self, oid: str, value_type: str, value: Union[str, int]) -> dict:
        """
        Performs an SNMP SET operation to update the value of a specified OID.

        Args:
            oid (str): The OID to update.
            value_type (str): The type of the value to set, uppercase or shortened version:
                'INTEGER' | 'i'
                'STRING' | 's'
                'IPADDRESS' | 'a'
                'COUNTER' | 'c'
                'GAUGE' | 'g'
                'TIMETICKS' | 't'
            value (str | int): The value to set.

        Returns:
            dict: The formatted response containing the status of the operation.
        """
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
