class ASN1Element:
    """
    Базовый класс для ASN.1 элементов. Определяет методы кодирования и декодирования длины.
    """
    @staticmethod
    def decode_length(data):
        length = data[0]
        if length & 0x80 == 0:
            return length, data[1:]
        num_bytes = length & 0x7F
        length = int.from_bytes(data[1:1+num_bytes], byteorder='big')
        return length, data[1+num_bytes:]

    @staticmethod
    def encode_length(length):
        if length < 128:
            return bytes([length])
        else:
            length_bytes = []
            while length > 0:
                length_bytes.insert(0, length & 0xFF)
                length = length >> 8
            return bytes([0x80 | len(length_bytes)] + bytes(length_bytes))


class ASN1Integer(ASN1Element):
    """
    ASN.1 INTEGER элемент.
    """
    @staticmethod
    def decode(data):
        length = data[1]
        value = int.from_bytes(data[2:2+length], byteorder='big')
        return value, data[2+length:]

    @staticmethod
    def encode(value):
        encoded_value = value.to_bytes((value.bit_length() + 7) // 8 or 1, byteorder='big', signed=True)
        return bytes([0x02]) + ASN1Element.encode_length(len(encoded_value)) + encoded_value


class ASN1OctetString(ASN1Element):
    """
    ASN.1 OCTET STRING элемент.
    """
    @staticmethod
    def decode(data):
        length = data[1]
        return data[2:2+length].decode(), data[2+length:]

    @staticmethod
    def encode(value):
        encoded_value = value.encode()
        return bytes([0x04]) + ASN1Element.encode_length(len(encoded_value)) + encoded_value


class ASN1Null(ASN1Element):
    """
    ASN.1 NULL элемент.
    """
    @staticmethod
    def decode(data):
        return None, data[2:]

    @staticmethod
    def encode():
        return bytes([0x05, 0x00])


class ASN1Oid(ASN1Element):
    """
    ASN.1 OID элемент.
    """
    @staticmethod
    def decode(data):
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

    @staticmethod
    def encode(oid):
        parts = list(map(int, oid.split('.')))
        
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
        return bytes([0x06, len(encoded_oid)]) + encoded_oid


class ASN1Tagged(ASN1Element):
    """
    ASN.1 любой другой элемент.
    """
    @staticmethod
    def decode(data):
        length, remaining_data = ASN1Element.decode_length(data[1:])
        return length, remaining_data
    
    @staticmethod
    def encode(tag, content):
        length = len(content)
        return bytes([tag]) + ASN1Element.encode_length(length) + content
