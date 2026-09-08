import pytest

class RateShape:
    SQUARE = "SQUARE"

class RateUnit:
    PER_SECOND = "PER_SECOND"

class NexmarkConfiguration:
    def __init__(self):
        self.numEvents = 0
        self.numEventGenerators = 1
        self.rateShape = RateShape.SQUARE
        self.firstEventRate = 10000
        self.nextEventRate = 10000
        self.rateUnit = RateUnit.PER_SECOND
        self.ratePeriodSec = 600
        self.preloadSeconds = 0
        self.streamTimeout = 240
        self.isRateLimited = False
        self.useWallclockEventTime = False
        self.personProportion = 1
        self.auctionProportion = 3
        self.bidProportion = 46
        self.avgPersonByteSize = 200
        self.avgAuctionByteSize = 500
        self.avgBidByteSize = 100
        self.hotAuctionRatio = 2
        self.hotSellersRatio = 4
        self.hotBiddersRatio = 4
        self.windowSizeSec = 10
        self.windowPeriodSec = 5
        self.watermarkHoldbackSec = 0
        self.numInFlightAuctions = 100
        self.numActivePeople = 1000

    def __eq__(self, other):
        return isinstance(other, NexmarkConfiguration) and self.__dict__ == other.__dict__
    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

class NexmarkUtils:
    RateShape = RateShape
    RateUnit = RateUnit

def test_default_values_are_not_all_custom():
    config = NexmarkConfiguration()
    assert config.numEvents != 1
    assert config.rateShape == RateShape.SQUARE
    assert config.firstEventRate != 20000
    assert config.rateUnit == RateUnit.PER_SECOND
    assert config.ratePeriodSec != 1200
    assert config.personProportion < config.bidProportion
    assert config.avgPersonByteSize != 300
    assert config.numInFlightAuctions != 999
    assert config.numActivePeople > 0

def test_equals_and_hashcode_diff_object():
    c1 = NexmarkConfiguration()
    c2 = NexmarkConfiguration()
    c1.firstEventRate = 12345
    assert c1 != c2
    c2.firstEventRate = 12345
    assert c1 == c2
    assert hash(c1) == hash(c2)