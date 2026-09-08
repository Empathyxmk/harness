import pytest
import json

class CpuMetric:
    def __init__(self, host, pid, cpu):
        self.host = host
        self.pid = pid
        self.cpu = cpu

    def __eq__(self, other):
        return isinstance(other, CpuMetric) and \
               self.host == other.host and \
               self.pid == other.pid and \
               self.cpu == other.cpu

    @staticmethod
    def from_json_array(json_str):
        arr = json.loads(json_str)
        return [CpuMetric(entry['host'], entry['pid'], entry['cpu']) for entry in arr]

def test_cpu_metric():
    cpu_metrics = [
        CpuMetric("10.0.0.12", 37927, 1.01),
        CpuMetric("10.1.0.33", 54389, 2.3),
        CpuMetric("10.2.0.44", 4401, 0.4),
    ]
    # Use list of dicts for json serialization
    dicts = [{"host": c.host, "pid": c.pid, "cpu": c.cpu} for c in cpu_metrics]
    json_str = json.dumps(dicts)
    expected = CpuMetric.from_json_array(json_str)
    assert expected == cpu_metrics