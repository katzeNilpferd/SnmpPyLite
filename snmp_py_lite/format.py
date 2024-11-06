class SNMPFormat:
    @staticmethod
    def formar_response(ip: str, status: str, raw_data: list) -> dict:
        formatted_answer = {
            'ip': ip,
            'status': status
        }
        
        if raw_data:
            formatted_answer.update({
                'version': raw_data[0],
                'community': raw_data[1],
                'request_id': raw_data[2],
                'error_status': raw_data[3],
                'error_index': raw_data[4],
                'data': {}
            })
            index = 5
            while index < len(raw_data):
                oid = raw_data[index]
                value = raw_data[index + 1]
                formatted_answer['data'][oid] = value
                index += 2

        return formatted_answer