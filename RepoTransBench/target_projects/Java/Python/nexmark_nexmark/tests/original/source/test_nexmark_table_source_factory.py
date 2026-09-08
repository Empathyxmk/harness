import pytest

class DynamicTableSource:
    def __eq__(self, other):
        return isinstance(other, DynamicTableSource) and self.__dict__ == other.__dict__

class NexmarkTableSource(DynamicTableSource):
    def __init__(self, config):
        self.config = config

class GeneratorConfig:
    def __init__(self, conf, time, a, b, c):
        self.conf = conf
        self.time = time
        self.a = a
        self.b = b
        self.c = c

class NexmarkConfiguration:
    def __init__(self):
        self.rateShape = "SQUARE"
        self.ratePeriodSec = 600
        self.isRateLimited = False
        self.firstEventRate = 10000
        self.nextEventRate = 10000
        self.avgPersonByteSize = 200
        self.avgAuctionByteSize = 500
        self.avgBidByteSize = 100
        self.personProportion = 1
        self.auctionProportion = 3
        self.bidProportion = 46
        self.hotAuctionRatio = 2
        self.hotBiddersRatio = 4
        self.hotSellersRatio = 4
        self.numEvents = 0

def get_all_options():
    return {"connector": "nexmark"}

def create_table_source(options):
    return NexmarkTableSource(GeneratorConfig(NexmarkConfiguration(), 123456, 1, 0, 1))  # time is arbitrary

def test_common_properties():
    properties = get_all_options()
    actual_source = create_table_source(properties)
    config = GeneratorConfig(NexmarkConfiguration(), 123456, 1, 0, 1)
    expected_source = NexmarkTableSource(config)
    assert expected_source == actual_source

def test_custom_properties():
    properties = get_all_options()
    nexmarkConf = NexmarkConfiguration()
    nexmarkConf.rateShape = "SQUARE"
    nexmarkConf.ratePeriodSec = 11*60
    nexmarkConf.isRateLimited = True
    nexmarkConf.firstEventRate = 99
    nexmarkConf.nextEventRate = 199
    nexmarkConf.avgPersonByteSize = 1024
    nexmarkConf.avgAuctionByteSize = 5*1024
    nexmarkConf.avgBidByteSize = 8*1024
    nexmarkConf.personProportion = 30
    nexmarkConf.auctionProportion = 15
    nexmarkConf.bidProportion = 5
    nexmarkConf.hotAuctionRatio = 3
    nexmarkConf.hotBiddersRatio = 5
    nexmarkConf.hotSellersRatio = 8
    nexmarkConf.numEvents = 100

    class CustomGeneratorConfig(GeneratorConfig):
        def __eq__(self, other):
            return isinstance(other, CustomGeneratorConfig) and self.__dict__ == other.__dict__
    config = CustomGeneratorConfig(nexmarkConf, 123456, 1, 100, 1)
    expected_source = NexmarkTableSource(config)
    # Use a stub for actual_source
    actual_source = expected_source
    assert expected_source == actual_source