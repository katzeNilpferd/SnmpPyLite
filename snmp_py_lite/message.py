from encoder import encode_integer, encode_oid, decode_integer, decode_oid, encode_null


class SNMPMessage:
    def __init__(self, version, community):
        self.version = version
        self.community = community

    def create_get_request(self, oid):
        # Создание сообщения для GET-запроса
        version_encoded = encode_integer(self.version)
        community_encoded = self.encode_string(self.community)
        oid_encoded = encode_oid(oid)

        # Формируем PDU
        request_id = encode_integer(1)  # Пример запроса с ID 1
        error_status = encode_integer(0)  # Ошибки нет
        error_index = encode_integer(0)   # Ошибки нет
        
        # Создание VarBind SEQUENCE (OID + NULL)
        varbind = bytes([0x30]) + self.encode_length(len(oid_encoded) + len(encode_null())) + oid_encoded + encode_null()
        varbind_list = bytes([0x30]) + self.encode_length(len(varbind)) + varbind

        # Создание PDU (GetRequest-PDU: 0xA0)
        pdu_content = request_id + error_status + error_index + varbind_list
        pdu = bytes([0xA0]) + self.encode_length(len(pdu_content)) + pdu_content

        # Создание полного сообщения SNMP
        message_content = version_encoded + community_encoded + pdu
        message = bytes([0x30]) + self.encode_length(len(message_content)) + message_content

        return message
        
    def parse_response(self, data):
        # Первый байт — это тег для последовательности, поэтому мы его пропускаем
        if data[0] != 0x30:  # 0x30 — тег для ASN.1 SEQUENCE
            raise ValueError("Ожидаем ASN.1 SEQUENCE")
        
        # Пропускаем длину (декодируем)
        _, data = self.decode_length(data[1:])
        
        # Парсим версию SNMP
        version, data = decode_integer(data)
        
        # Парсим строку community
        community, data = self.decode_string(data)

        # Парсим PDU
        if data[0] != 0xA2:  # 0xA2 — это GetResponse-PDU
            raise ValueError("Ожидаем GetResponse-PDU")
        
        _, data = self.decode_length(data[1:])
        
        # Парсим идентификатор запроса
        request_id, data = decode_integer(data)
        
        # Парсим статус ошибки
        error_status, data = decode_integer(data)
        
        # Парсим индекс ошибки
        error_index, data = decode_integer(data)
        
        # Парсим VarBindList (начинается с тега 0x30, SEQUENCE)
        if data[0] != 0x30:
            raise ValueError("Ожидаем VarBindList (SEQUENCE)")
        
        _, data = self.decode_length(data[1:])
        
        # Теперь парсим VarBind (OID и значение)
        if data[0] != 0x30:
            raise ValueError("Ожидаем VarBind (SEQUENCE)")
        
        _, data = self.decode_length(data[1:])
        
        # Парсим OID
        oid, data = decode_oid(data)
        
        # Парсим значение (значение может быть различных типов, обработаем целое число для примера)
        if data[0] == 0x02:  # 0x02 — это целое число
            value, data = decode_integer(data)
        elif data[0] == 0x04:  # 0x04 — это строка
            value, data = self.decode_string(data)
        elif data[0] == 0x05:  # 0x05 — это NULL
            value = None
            data = data[2:]  # Пропускаем тег и длину
        
        # Возвращаем результат
        return oid, value, version, community
    
    def encode_string(self, string):
        length = len(string)
        return bytes([0x04, length]) + string.encode()
    
    def decode_string(self, data):
        if data[0] != 0x04:
            raise ValueError('Ожидаемый строковый тег')
        length = data[1]
        return data[2:2+length].decode(), data[2+length:]
    
    def encode_length(self, length):
        if length < 128:
            return bytes([length])
        else:
            length_bytes = []
            while length > 0:
                length_bytes.insert(0, length & 0xFF)
                length = length >> 8
            return bytes([0x80 | len(length_bytes)] + bytes(length_bytes))

    def decode_length(self, data):
        length = data[0]
        if length & 0x80 == 0:
            return length, data[1:]
        num_bytes = length & 0x7F
        length = int.from_bytes(data[1:1+num_bytes], byteorder='big')
        return length, data[1+num_bytes:]
