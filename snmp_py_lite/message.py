from encoder import *


class SNMPMessage:
    def __init__(self, version, community):
        self.version = version
        self.community = community
        
        self.value_tag = {
            0x02: ASN1Integer,
            0x04: ASN1OctetString,
            0x05: ASN1Null,
            0x06: ASN1Oid
        }
    
    def create_get_request(self, oid):
        version_encoded = ASN1Integer.encode(self.version)
        community_encoded = ASN1OctetString.encode(self.community)
        pdu = PDU.create_get_request_pdu(oid)

        message_content = version_encoded + community_encoded + pdu
        message = ASN1Tagged.encode(0x30, message_content)
        
        return message
        
    def parse_response(self, data):
        self._check_integrity(data)

        list_value = []
        while data:
            decoder_class = self.value_tag.get(data[0])
            
            if decoder_class is None:
                decoder_class = ASN1Tagged()
                _, data = decoder_class.decode(data)
            else:
                value, data = decoder_class.decode(data)
                list_value.append(value)
                
        return list_value
    
    def _check_integrity(self, data):
        if data[0] != 0x30:
            raise ValueError("Ожидается ASN.1 SEQUENCE")
        expected_length, remaining_data = ASN1Element.decode_length(data[1:])
        if len(remaining_data) != expected_length:
            raise ValueError(f"Неполные данные: ожидается {expected_length} байт, но получено {len(remaining_data)} байт")


class PDU:
    @staticmethod
    def create_get_request_pdu(oid):
        request_id = ASN1Integer.encode(1)
        error_status = ASN1Integer.encode(0)
        error_index = ASN1Integer.encode(0)
        oid_encoded = ASN1Oid.encode(oid)
        
        varbind = VarBind.create_varbind(oid_encoded, ASN1Null.encode())
        varbind_list = ASN1Tagged.encode(0x30, varbind)

        pdu_content = request_id + error_status + error_index + varbind_list
        pdu = ASN1Tagged.encode(0xA0, pdu_content)
        return pdu


class VarBind:
    @staticmethod
    def create_varbind(oid_encoded, value_encoded):
        varbind_content = oid_encoded + value_encoded
        return ASN1Tagged.encode(0x30, varbind_content)
