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
        if not isinstance(value, int):
            raise TypeError(f'Value: {value} must be an integer')
        
        encoded_value = value.to_bytes((value.bit_length() + 7) // 8 or 1, byteorder='big', signed=True)
        return bytes([0x02]) + ASN1Element.encode_length(len(encoded_value)) + encoded_value


class ASN1OctetString(ASN1Element):
    """
    ASN.1 OCTET STRING элемент.
    """
    @staticmethod
    def decode(data):
        length = data[1]
        
        if length & 0x80:
            num_length_bytes = length & 0x7F
            length = int.from_bytes(data[2:2 + num_length_bytes], 'big')
            raw_bytes_start = 2 + num_length_bytes
        else:
            raw_bytes_start = 2
        
        raw_bytes = data[raw_bytes_start:raw_bytes_start + length]
        
        try:
            # Пробуем декодировать как UTF-8 строку
            decoded_string = raw_bytes.decode('utf-8')
        except UnicodeDecodeError:
            # Если декодирование не удается, возвращаем raw байты в hex формате
            decoded_string = raw_bytes.hex()  # или просто raw_bytes, если так нужно
        
        return decoded_string, data[raw_bytes_start + length:]

    @staticmethod
    def encode(value):
        if not isinstance(value, str):
            raise TypeError(f'Value: {value} must be an string')
        
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
        try:
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
        
        except Exception as e:
            raise ValueError(f'Oid: {oid} has incorrect format')


class ASN1IpAddress(ASN1Element):
    """
    ASN.1 IpAddress элемент.
    """
    @staticmethod
    def decode(data):
        length = data[1]
        if length != 4:
            raise ValueError("IPAddress must be 4 bytes long")
        ip_bytes = data[2:6]
        ip_address = ".".join(map(str, ip_bytes))  # Преобразование в строковый формат IP
        return ip_address, data[6:]

    @staticmethod
    def encode(ip_address):
        ip_parts = ip_address.split(".")
        if len(ip_parts) != 4:
            raise ValueError("Invalid ip format")
        ip_bytes = bytes(map(int, ip_parts))
        return bytes([0x40]) + ASN1Element.encode_length(4) + ip_bytes


class ASN1Counter32(ASN1Element):
    """
    ASN.1 Counter32 элемент.
    """
    @staticmethod
    def decode(data):
        length = data[1]
        value = int.from_bytes(data[2:2+length], byteorder='big')
        return value, data[2+length:]

    @staticmethod
    def encode(value):
        if not isinstance(value, int) or value < 0 or value > 0xFFFFFFFF:
            raise ValueError("Counter32 must be a positive integer and not exceed 32 bits")
        encoded_value = value.to_bytes(4, byteorder='big')  # Counter32 всегда 4 байта
        return bytes([0x41]) + ASN1Element.encode_length(len(encoded_value)) + encoded_value


class ASN1Gauge(ASN1Element):
    """
    ASN.1 Gauge32 элемент.
    """
    @staticmethod
    def decode(data):
        length = data[1]
        value = int.from_bytes(data[2:2+length], byteorder='big')
        return value, data[2+length:]

    @staticmethod
    def encode(value):
        encoded_value = value.to_bytes((value.bit_length() + 7) // 8 or 1, byteorder='big', signed=False)
        return bytes([0x42]) + ASN1Element.encode_length(len(encoded_value)) + encoded_value


class ASN1TimeTicks(ASN1Element):
    """
    ASN.1 TimeTicks элемент.
    """
    @staticmethod
    def decode(data):
        if data[0] != 0x43:
            raise ValueError("Invalid TimeTicks tag")
        length = data[1]
        value = int.from_bytes(data[2:2+length], byteorder='big')
        return value, data[2+length:]

    @staticmethod
    def encode(value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("TimeTicks must be a positive integer")
        encoded_value = value.to_bytes((value.bit_length() + 7) // 8 or 1, byteorder='big')
        return bytes([0x43]) + ASN1Element.encode_length(len(encoded_value)) + encoded_value


class ASN1Counter64(ASN1Element):
    """
    ASN.1 Counter64 элемент.
    """
    @staticmethod
    def decode(data):
        length = data[1]
        value = int.from_bytes(data[2:2+length], byteorder='big')
        return value, data[2+length:]

    @staticmethod
    def encode(value):
        if not isinstance(value, int) or value < 0 or value > 0xFFFFFFFFFFFFFFFF:
            raise ValueError("Counter64 must be a positive integer and not exceed 64 bits")
        encoded_value = value.to_bytes(8, byteorder='big')  # Counter64 всегда 8 байт
        return bytes([0x46]) + ASN1Element.encode_length(len(encoded_value)) + encoded_value


class ASN1EndOfMibView(ASN1Element):
    """
    ASN.1 EndOfMibView элемент.
    """
    @staticmethod
    def decode(data):
        # Длина всегда должна быть 0
        length = data[1]
        if length != 0:
            raise ValueError("EndOfMibView must have a length of 0")
        return 'endOfMibView', data[2:]

    @staticmethod
    def encode():
        return bytes([0x82, 0x00])  # ASN.1 тег для EndOfMibView с нулевой длиной


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
