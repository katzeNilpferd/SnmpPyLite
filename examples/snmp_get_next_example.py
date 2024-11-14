from snmp_py_lite.client import SNMPClient

client = SNMPClient(ip='192.168.126.10', version=1)
response = client.get_next('1.3.6.1.2.1.1.1.0')

print(response)

"""
    {'ip': '192.168.126.10',
    'version': 1,
    'community': 'public',
    'request_id': 1732154153,
    'error_status': 0,
    'error_index': 0,
    'data': {'1.3.6.1.2.1.1.2.0': '1.3.6.1.4.1.171.10.75.15.2'}
    }
"""