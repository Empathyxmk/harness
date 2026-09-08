import base64

class BasicAuth:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def generate_headers(self):
        creds = f"{self.username}:{self.password}"
        encoded = base64.b64encode(creds.encode('utf-8')).decode('ascii')
        return {"Authorization": f"Basic {encoded}"}

    def attach(self, req):
        if hasattr(req, "headers"):
            req.headers.update(self.generate_headers())

    def __repr__(self):
        return f"<BasicAuth username={self.username}>"

class BearerToken:
    def __init__(self, token):
        self.token = token

    def generate_headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    def attach(self, req):
        if hasattr(req, "headers"):
            req.headers.update(self.generate_headers())

    def __repr__(self):
        return f"<BearerToken ...>"

class ApiKey:
    def __init__(self, key, value, in_header=True):
        self.key = key
        self.value = value
        self.in_header = in_header

    def generate_headers(self):
        if self.in_header:
            return {self.key: self.value}
        else:
            print("application/xml not supported yet!")
            return {}

    def attach(self, req):
        if hasattr(req, "headers") and self.in_header:
            req.headers.update(self.generate_headers())

    def __repr__(self):
        return f"<ApiKey key={self.key} in_header={self.in_header}>"