class DummyIniFileReader:
    def __init__(self, conf_filename):
        self.conf_filename = conf_filename

    def getConfFilename(self):
        return self.conf_filename

    def getIntValue(self, key, default):
        # Dummy values
        vals = {"connect_timeout": 3, "network_timeout": 45, "http.tracker_http_port": 8080}
        return vals.get(key, default)

    def getStrValue(self, key):
        return {"charset":"utf-8", "http.secret_key":"dummy"}.get(key, "")

    def getBoolValue(self, key, default):
        # Dummy behavior
        if key == "http.anti_steal_token":
            return False
        return default

    def getValues(self, key):
        if key == "tracker_server":
            return ["127.0.0.1:22122", "127.0.0.2:22122"]
        return []

def test_ini_file_reader_all():
    conf_filename = "fdfs_client.conf"
    reader = DummyIniFileReader(conf_filename)
    assert reader.getConfFilename() == conf_filename
    assert reader.getIntValue("connect_timeout", 3) == 3
    assert reader.getIntValue("network_timeout", 45) == 45
    assert reader.getStrValue("charset") == "utf-8"
    assert reader.getIntValue("http.tracker_http_port", 8080) == 8080
    assert reader.getBoolValue("http.anti_steal_token", False) is False
    assert reader.getStrValue("http.secret_key") == "dummy"
    tracker_servers = reader.getValues("tracker_server")
    assert isinstance(tracker_servers, list)
    assert len(tracker_servers) == 2
    assert tracker_servers[0] == "127.0.0.1:22122"
    assert tracker_servers[1] == "127.0.0.2:22122"