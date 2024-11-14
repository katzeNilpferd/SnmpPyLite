from snmp_py_lite.client import SNMPClient

client = SNMPClient(ip='192.168.126.10', version=1)
response = client.get('1.3.6.1.2.1.1.1.0')

print(response)

"""
    {'ip': '192.168.126.10',
    'version': 1,
    'community': 'public',
    'request_id': 1732171134,
    'error_status': 0,
    'error_index': 0,
    'data': {'1.3.6.1.2.1.1.1.0': 'DES-1210-28/ME/B2'}
    }
"""