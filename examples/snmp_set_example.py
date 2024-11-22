from snmp_py_lite.client import SNMPClient

client = SNMPClient(ip='192.168.126.10', version='1', community='private')
response = client.set('1.3.6.1.2.1.2.2.1.7.5', value_type='INTEGER', value=2)
# Disable port 5. A numeric value is transmitted, of which 1 is the on state, 2 is the off state.
print(response)

"""
    {'ip': '192.168.126.10',
    'version': 1,
    'community': 'private',
    'request_id': 1732336125,
    'error_status': 0,
    'error_index': 0,
    'data': {'1.3.6.1.2.1.2.2.1.7.5': 2}
    }
"""