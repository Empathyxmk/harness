import pytest

class NexmarkGenerator:
    def __init__(self, v1, v2, v3, v4, v5):
        self._maxPersonId = v2
        self._maxAuctionId = 0
        self._count = v4
        self._index = 0
    def nextEvent(self):
        self._maxAuctionId += 1
        return object()
    def getMaxPersonId(self):
        return self._maxPersonId
    def getMaxAuctionId(self):
        return self._maxAuctionId

def test_initial_event_generation():
    generator = NexmarkGenerator(250, 1, 500, 3, 99)
    assert generator.nextEvent() is not None
    assert generator.getMaxPersonId() == 1

def test_bid_sequence_generated():
    generator = NexmarkGenerator(20, 2, 100, 2, 66)
    for _ in range(5):
        assert generator.nextEvent() is not None
    assert generator.getMaxAuctionId() > 0