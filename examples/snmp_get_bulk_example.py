from snmp_py_lite.client import SNMPClient

client = SNMPClient(ip='192.168.126.10', version='2c')
response = client.get_bulk('1.3.6.1.2.1.1.1.0')

print(response)

"""
    {'ip': '192.168.126.10',
    'version': 1,
    'community': 'public',
    'request_id': 1732189878,
    'error_status': noError(0),
    'error_index': 0,
    'data': {'1.3.6.1.2.1.1.2.0': '1.3.6.1.4.1.171.10.75.15.2',
            '1.3.6.1.2.1.1.3.0': 70921899,
            '1.3.6.1.2.1.1.4.0': 'noc@dec.net.ua',
            '1.3.6.1.2.1.1.5.0': '192.168.126.10',
            '1.3.6.1.2.1.1.6.0': 'dpsh23-0-33d28-des1210me',
            '1.3.6.1.2.1.1.7.0': 72,
            '1.3.6.1.2.1.1.8.0': 70921740,
            '1.3.6.1.2.1.1.9.1.2.1': '1.3.6.1.2.1.2',
            '1.3.6.1.2.1.1.9.1.2.2': '1.3.6.1.2.1.10.7.2',
            '1.3.6.1.2.1.1.9.1.2.3': '1.3.6.1.2.1.158.1.1',
            '1.3.6.1.2.1.1.9.1.2.4': '1.0.8802.1.1.1.1.1',
            '1.3.6.1.2.1.1.9.1.2.5': '1.3.6.1.2.1.17.7.1.2',
            '1.3.6.1.2.1.1.9.1.2.6': '1.3.6.1.2.1.17.4.5',
            '1.3.6.1.2.1.1.9.1.2.7': '1.3.6.1.2.1.17',
            '1.3.6.1.2.1.1.9.1.2.8': '1.3.6.1.2.1.4',
            '1.3.6.1.2.1.1.9.1.2.9': '1.3.6.1.2.1.81',
            '1.3.6.1.2.1.1.9.1.2.10': '1.3.6.1.2.1.80',
            '1.3.6.1.2.1.1.9.1.2.11': '1.3.6.1.2.1.1',
            '1.3.6.1.2.1.1.9.1.2.12': '1.3.6.1.2.1.6',
            '1.3.6.1.2.1.1.9.1.2.13': '1.3.6.1.2.1.67.2.2.1.1'}
    }
"""