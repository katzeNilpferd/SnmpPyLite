import pytest
from snmp_py_lite import SNMPClient

@pytest.fixture
def client():
    return SNMPClient(ip='192.168.126.10', version=1)


def test_get_request(client):
    response = client.get('1.3.6.1.2.1.1.1.0')
    assert isinstance(response, dict), 'Ответ должен быть словарём'
    assert 'ip' in response, 'Ответ должет содержать ключ "ip"'


def test_get_next_request(client):
    response = client.get_next('1.3.6.1.2.1.1.1.0')
    assert isinstance(response, dict), 'Ответ должен быть словарём'
    assert 'ip' in response, 'Ответ должет содержать ключ "ip"'


def test_get_bulk_request(client):
    response = client.get_bulk('1.3.6.1.2.1.1.1.0')
    assert isinstance(response, dict), 'Ответ должен быть словарём'
    assert 'ip' in response, 'Ответ должет содержать ключ "ip"'


# def test_invalid_oid(client):
#     with pytest.raises(Exception):
#         client.get('invalid_oid')