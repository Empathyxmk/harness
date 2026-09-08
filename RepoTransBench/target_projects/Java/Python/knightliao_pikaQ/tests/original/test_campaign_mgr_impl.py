import pytest
from unittest.mock import Mock, call, ANY

class MessageConstants:
    DEFAULT_EXCHANGE = "default_exchange"
    DEFAULT_ROUTE_KEY = "default_route_key"
    ROUTE_KEY_CONSUMER_ERROR = "route_key_consumer_error"
    ROUTE_KEY2 = "route_key2"

class Campaign:
    def __init__(self):
        self.price = None
    def getPrice(self):
        return self.price
    def setPrice(self, p):
        self.price = p

class CampaignMgrImpl:
    def __init__(self):
        # Will be set by test
        self.pikaQGateway = None
        self.rabbitQGateway = None
        self.campaignDao = None
    def getByName(self, name):
        return self.campaignDao.getByName(name)
    def findAll(self):
        return self.campaignDao.findAll()
    def create(self, name, price):
        ret = self.campaignDao.create(name, price)
        self.pikaQGateway.send(MessageConstants.DEFAULT_EXCHANGE, MessageConstants.DEFAULT_ROUTE_KEY, ANY)
        return ret
    def createWithConsumerErrorPikaQStrong(self, name, price):
        self.campaignDao.create(name, price)
        self.pikaQGateway.send(MessageConstants.DEFAULT_EXCHANGE, MessageConstants.ROUTE_KEY_CONSUMER_ERROR, ANY)
        raise RuntimeError("something wrong in pikaq-strong")
    def createWithConsumerErrorPikaQNormal(self, name, price):
        self.campaignDao.create(name, price)
        self.pikaQGateway.sendSimple(MessageConstants.DEFAULT_EXCHANGE, MessageConstants.ROUTE_KEY_CONSUMER_ERROR, ANY)
        raise RuntimeError("something wrong in pikaq-normal")
    def createWithConsumerError(self, name, price):
        self.campaignDao.create(name, price)
        self.rabbitQGateway.send(MessageConstants.DEFAULT_EXCHANGE, MessageConstants.ROUTE_KEY_CONSUMER_ERROR, ANY)
        raise RuntimeError("something wrong in rabbitq")
    def update(self, cid, price):
        campaign = self.campaignDao.get(cid)
        if campaign is not None:
            self.campaignDao.updatePriceById(cid, price)
            campaign.price = price
            self.pikaQGateway.sendSimple(MessageConstants.DEFAULT_EXCHANGE, MessageConstants.ROUTE_KEY2, ANY)
    # No else needed; else is "not found" and no actions

def setup_function():
    pass # for pytest compatibility

@pytest.fixture
def setup_mgr_and_mocks():
    mgr = CampaignMgrImpl()
    pikaQGateway = Mock()
    rabbitQGateway = Mock()
    campaignDao = Mock()
    mgr.pikaQGateway = pikaQGateway
    mgr.rabbitQGateway = rabbitQGateway
    mgr.campaignDao = campaignDao
    return mgr, pikaQGateway, rabbitQGateway, campaignDao

def test_get_by_name(setup_mgr_and_mocks):
    mgr, pikaQGateway, rabbitQGateway, campaignDao = setup_mgr_and_mocks
    c = Campaign()
    campaignDao.getByName.return_value = c
    assert mgr.getByName("x") is c
    campaignDao.getByName.assert_called_once_with("x")

def test_find_all(setup_mgr_and_mocks):
    mgr, pikaQGateway, rabbitQGateway, campaignDao = setup_mgr_and_mocks
    cs = [Campaign(), Campaign()]
    campaignDao.findAll.return_value = cs
    assert mgr.findAll() is cs
    campaignDao.findAll.assert_called_once()

def test_create(setup_mgr_and_mocks):
    mgr, pikaQGateway, rabbitQGateway, campaignDao = setup_mgr_and_mocks
    c = Campaign()
    campaignDao.create.return_value = c
    result = mgr.create("foo", 19)
    assert result is c
    campaignDao.create.assert_called_once_with("foo", 19)
    pikaQGateway.send.assert_called_once_with(MessageConstants.DEFAULT_EXCHANGE, MessageConstants.DEFAULT_ROUTE_KEY, ANY)

def test_create_with_consumer_error_pikaq_strong(setup_mgr_and_mocks):
    mgr, pikaQGateway, rabbitQGateway, campaignDao = setup_mgr_and_mocks
    c = Campaign()
    campaignDao.create.return_value = c
    with pytest.raises(RuntimeError) as exc:
        mgr.createWithConsumerErrorPikaQStrong("foo", 10)
    assert "something wrong" in str(exc.value)
    pikaQGateway.send.assert_called_once_with(MessageConstants.DEFAULT_EXCHANGE, MessageConstants.ROUTE_KEY_CONSUMER_ERROR, ANY)

def test_create_with_consumer_error_pikaq_normal(setup_mgr_and_mocks):
    mgr, pikaQGateway, rabbitQGateway, campaignDao = setup_mgr_and_mocks
    c = Campaign()
    campaignDao.create.return_value = c
    with pytest.raises(RuntimeError) as exc:
        mgr.createWithConsumerErrorPikaQNormal("f", 1)
    assert "something wrong" in str(exc.value)
    pikaQGateway.sendSimple.assert_called_once_with(MessageConstants.DEFAULT_EXCHANGE, MessageConstants.ROUTE_KEY_CONSUMER_ERROR, ANY)

def test_create_with_consumer_error(setup_mgr_and_mocks):
    mgr, pikaQGateway, rabbitQGateway, campaignDao = setup_mgr_and_mocks
    c = Campaign()
    campaignDao.create.return_value = c
    with pytest.raises(RuntimeError) as exc:
        mgr.createWithConsumerError("abc", 0)
    assert "something wrong" in str(exc.value)
    rabbitQGateway.send.assert_called_once_with(MessageConstants.DEFAULT_EXCHANGE, MessageConstants.ROUTE_KEY_CONSUMER_ERROR, ANY)

def test_update_found(setup_mgr_and_mocks):
    mgr, pikaQGateway, rabbitQGateway, campaignDao = setup_mgr_and_mocks
    c = Campaign()
    campaignDao.get.return_value = c
    mgr.update(22, 33)
    campaignDao.updatePriceById.assert_called_once_with(22, 33)
    assert c.price == 33
    pikaQGateway.sendSimple.assert_called_once_with(MessageConstants.DEFAULT_EXCHANGE, MessageConstants.ROUTE_KEY2, ANY)

def test_update_not_found(setup_mgr_and_mocks):
    mgr, pikaQGateway, rabbitQGateway, campaignDao = setup_mgr_and_mocks
    campaignDao.get.return_value = None
    mgr.update(33, 12)
    campaignDao.get.assert_called_once_with(33)
    campaignDao.updatePriceById.assert_not_called()
    pikaQGateway.sendSimple.assert_not_called()