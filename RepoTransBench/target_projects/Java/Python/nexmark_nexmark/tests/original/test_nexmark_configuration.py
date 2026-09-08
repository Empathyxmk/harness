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

def test_default_values():
    config = NexmarkConfiguration()
    assert config.numEvents == 0
    assert config.numEventGenerators == 1
    assert config.rateShape == RateShape.SQUARE
    assert config.firstEventRate == 10000
    assert config.nextEventRate == 10000
    assert config.rateUnit == RateUnit.PER_SECOND
    assert config.ratePeriodSec == 600
    assert config.preloadSeconds == 0
    assert config.streamTimeout == 240
    assert config.isRateLimited == False
    assert config.useWallclockEventTime == False
    assert config.personProportion == 1
    assert config.auctionProportion == 3
    assert config.bidProportion == 46
    assert config.avgPersonByteSize == 200
    assert config.avgAuctionByteSize == 500
    assert config.avgBidByteSize == 100
    assert config.hotAuctionRatio == 2
    assert config.hotSellersRatio == 4
    assert config.hotBiddersRatio == 4
    assert config.windowSizeSec == 10
    assert config.windowPeriodSec == 5
    assert config.watermarkHoldbackSec == 0
    assert config.numInFlightAuctions == 100
    assert config.numActivePeople == 1000

def test_equals_and_hashcode():
    c1 = NexmarkConfiguration()
    c2 = NexmarkConfiguration()
    assert c1 == c2
    assert hash(c1) == hash(c2)
    c2.numEvents = 100
    assert c1 != c2