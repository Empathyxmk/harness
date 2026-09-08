import pytest

class ProtostuffSerializer:
    def write_request(self, buf, request):
        buf.append(f"Request:{request['request_id']}:{request['service_id']}")
    def read_request(self, buf):
        if not buf:
            return None
        raw = buf.pop(0)
        request_id, service_id = raw.replace("Request:", "").split(":")
        return {"request_id": int(request_id), "service_id": int(service_id)}
    def write_response(self, buf, response):
        buf.append(f"Response:{response['request_id']}:{response['status_code']}:{response['result']}")
    def read_response(self, buf):
        if not buf:
            return None
        raw = buf.pop(0)
        _, request_id, status_code, result = raw.split(":")
        return {"request_id": int(request_id), "status_code": int(status_code), "result": result}

def test_protostuff_serializer_request_and_response():
    serializer = ProtostuffSerializer()
    buf = []
    request = {"request_id": 123, "service_id": 8}
    serializer.write_request(buf, request)
    # simulate seeking reader index
    read_request = serializer.read_request(buf)
    assert read_request == {"request_id": 123, "service_id": 8}

    buf.clear()
    response = {"request_id": 321, "status_code": 1, "result": "userlist"}
    serializer.write_response(buf, response)
    read_response = serializer.read_response(buf)
    assert read_response == {"request_id": 321, "status_code": 1, "result": "userlist"}