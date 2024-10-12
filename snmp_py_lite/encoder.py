def encode_integer(value):
    if not isinstance(value, int):
        raise ValueError("Значение для кодирования должно быть целым числом")
    if value < 0:
        raise ValueError("SNMP поддерживает только положительные целые числа")
    
    encoded_value = b''
    while value > 0:
        encoded_value = bytes([value & 0xFF]) + encoded_value
        value = value >> 8
    if not encoded_value:
        encoded_value = b'\x00'
    length = len(encoded_value)
    return bytes([0x02, length]) + encoded_value  # 0x02 — это тег для целого числа


def decode_integer(data):
    if data[0] != 0x02:
        raise ValueError("Неверный тег для целого числа")
    length = data[1]
    value = int.from_bytes(data[2:2+length], byteorder='big')
    return value, data[2+length:]


def encode_oid(oid):
    parts = list(map(int, oid.split('.')))
    if len(parts) < 2:
        raise ValueError("OID должен содержать хотя бы два элемента")
    encoded_oid = bytes([(40 * parts[0]) + parts[1]])
    for part in parts[2:]:
        if part == 0:
            encoded_oid += bytes([0])
        else:
            encoded_part = []
            while part > 0:
                encoded_part.insert(0, (part & 0x7F) | 0x80)
                part = part >> 7
            if encoded_part:
                encoded_part[-1] &= 0x7F
            encoded_oid += bytes(encoded_part)
    return bytes([0x06, len(encoded_oid)]) + encoded_oid  # 0x06 — это тег для OID


def decode_oid(data):
    if data[0] != 0x06:
        raise ValueError("Неверный тег для OID")
    length = data[1]
    oid_bytes = data[2:2+length]
    first_byte = oid_bytes[0]
    oid = [first_byte // 40, first_byte % 40]
    part = 0
    for byte in oid_bytes[1:]:
        part = (part << 7) | (byte & 0x7F)
        if byte & 0x80 == 0:
            oid.append(part)
            part = 0
    return '.'.join(map(str, oid)), data[2+length:]


def encode_null():
    return bytes([0x05, 0x00])  # 0x05 — это тег для NULL

