import pytest
import json

class TpsMetric:
    def __init__(self, id_val, min_val, max_val, avg_val, sum_val):
        self.id = id_val
        self.min = min_val
        self.max = max_val
        self.avg = avg_val
        self.sum = sum_val

    def __eq__(self, other):
        return (isinstance(other, TpsMetric)
                and self.id == other.id
                and self.min == other.min
                and self.max == other.max
                and self.avg == other.avg
                and self.sum == other.sum)

    @classmethod
    def from_json(cls, json_str):
        arr = json.loads(json_str)
        item = arr[0]
        return cls(item["id"], item["min"], item["max"], item["avg"], item["sum"])

def test_parse_json():
    json_str = """
    [
    {
    "id": "Source__TableSourceScan(table=[[default_catalog__default_database__nexmark]]__fi.numRecordsOutPerSecond",
    "min": 5003.2,
    "max": 5003.2,
    "avg": 5003.2,
    "sum": 10006.3
    }
    ]
    """
    tps = TpsMetric.from_json(json_str)
    expected = TpsMetric(
        "Source__TableSourceScan(table=[[default_catalog__default_database__nexmark]]__fi.numRecordsOutPerSecond",
        5003.2,
        5003.2,
        5003.2,
        10006.3
    )
    assert tps == expected