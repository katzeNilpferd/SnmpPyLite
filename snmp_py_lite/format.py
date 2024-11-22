import re
from .constants import ERROR_STATUS


class SNMPFormat:
    @staticmethod
    def format_oid(oid: str) -> str:
        if oid.startswith("."):
            oid = oid[1:]

        if not re.match(r'^\d+(\.\d+)*$', oid):
            raise ValueError(f"Invalid OID: {oid}")

        return oid
    
    @staticmethod
    def formar_response(ip: str, raw_data: list) -> dict:
        formatted_answer = {
            'ip': ip,
            'version': raw_data[0],
            'community': raw_data[1],
            'request_id': raw_data[2],
            'error_status': f'{ERROR_STATUS[raw_data[3]]}({raw_data[3]})',
            'error_index': raw_data[4],
            'data': {}
        }
        index = 5
        while index < len(raw_data):
            oid = raw_data[index]
            value = raw_data[index + 1] if index + 1 < len(raw_data) else None
            formatted_answer['data'][oid] = value
            index += 2

        return formatted_answer