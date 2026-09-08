import socket

class FileBackend:
    def __init__(self, filename):
        self.filename = filename

    def send_metric(self, metric):
        with open(self.filename, "a") as f:
            f.write(f"{metric.host} {metric.service} {metric.metric} {metric.value} {metric.timestamp}\n")

class CarbonBackend:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send_metric(self, metric):
        line = f"{metric.host}.{metric.service}.{metric.metric} {metric.value} {metric.timestamp}\n"
        sock = socket.socket()
        try:
            sock.connect((self.host, self.port))
            sock.sendall(line.encode())
        finally:
            sock.close()

class UDPSendBackend:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send_metric(self, metric):
        line = f"{metric.host}.{metric.service}.{metric.metric} {metric.value} {metric.timestamp}"
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.sendto(line.encode(), (self.host, self.port))
        finally:
            sock.close()

def load_backend(name, *args, **kwargs):
    name = name.lower()
    if name == "file":
        return FileBackend(*args, **kwargs)
    elif name == "carbon":
        return CarbonBackend(*args, **kwargs)
    elif name == "udp":
        return UDPSendBackend(*args, **kwargs)
    else:
        raise ValueError(f"Unknown backend {name}")