package original

import (
	"math/big"
	"testing"
)

type Campaign struct {
	Price *big.Float
}

type CampaignDao interface {
	GetByName(name string) *Campaign
	FindAll() []*Campaign
	Create(name string, price *big.Float) *Campaign
	Get(id int64) *Campaign
	UpdatePriceById(id int64, price *big.Float)
}

type PikaQGateway interface {
	Send(exchange, routeKey string, msg interface{})
	SendSimple(exchange, routeKey string, msg interface{})
}
type RabbitQGateway interface {
	Send(exchange, routeKey string, msg interface{})
	SendSimple(exchange, routeKey string, msg interface{})
}

var (
	DEFAULT_EXCHANGE = "defaultExchange"
	DEFAULT_ROUTE_KEY = "defaultRouteKey"
	ROUTE_KEY_CONSUMER_ERROR = "routeKeyConsumerError"
	ROUTE_KEY2 = "routeKey2"
)

type FakeCampaignDao struct {
	getByNameResp map[string]*Campaign
	findAllResp   []*Campaign
	createResp    *Campaign
	getResp       map[int64]*Campaign
	updatePrice   map[int64]*big.Float
}
func (f *FakeCampaignDao) GetByName(name string) *Campaign {
	return f.getByNameResp[name]
}
func (f *FakeCampaignDao) FindAll() []*Campaign {
	return f.findAllResp
}
func (f *FakeCampaignDao) Create(name string, price *big.Float) *Campaign {
	return f.createResp
}
func (f *FakeCampaignDao) Get(id int64) *Campaign {
	return f.getResp[id]
}
func (f *FakeCampaignDao) UpdatePriceById(id int64, price *big.Float) {
	if f.updatePrice == nil {
		f.updatePrice = map[int64]*big.Float{}
	}
	f.updatePrice[id] = price
}

type MsgLog struct {
	Called bool
	Args   []interface{}
}
type FakePikaQGateway struct{ SendLog, SendSimpleLog MsgLog }
func (f *FakePikaQGateway) Send(exchange, routeKey string, msg interface{}) {
	f.SendLog.Called = true
	f.SendLog.Args = []interface{}{exchange, routeKey, msg}
}
func (f *FakePikaQGateway) SendSimple(exchange, routeKey string, msg interface{}) {
	f.SendSimpleLog.Called = true
	f.SendSimpleLog.Args = []interface{}{exchange, routeKey, msg}
}
type FakeRabbitQGateway struct{ SendLog, SendSimpleLog MsgLog }
func (f *FakeRabbitQGateway) Send(exchange, routeKey string, msg interface{}) {
	f.SendLog.Called = true
	f.SendLog.Args = []interface{}{exchange, routeKey, msg}
}
func (f *FakeRabbitQGateway) SendSimple(exchange, routeKey string, msg interface{}) {
	f.SendSimpleLog.Called = true
	f.SendSimpleLog.Args = []interface{}{exchange, routeKey, msg}
}

type CampaignMgrImpl struct {
	PikaQGateway  PikaQGateway
	RabbitQGateway RabbitQGateway
	CampaignDao    CampaignDao
}

func (mgr *CampaignMgrImpl) GetByName(name string) *Campaign {
	return mgr.CampaignDao.GetByName(name)
}
func (mgr *CampaignMgrImpl) FindAll() []*Campaign {
	return mgr.CampaignDao.FindAll()
}
func (mgr *CampaignMgrImpl) Create(name string, price *big.Float) *Campaign {
	c := mgr.CampaignDao.Create(name, price)
	mgr.PikaQGateway.Send(DEFAULT_EXCHANGE, DEFAULT_ROUTE_KEY, nil)
	return c
}
func (mgr *CampaignMgrImpl) CreateWithConsumerErrorPikaQStrong(name string, price *big.Float) {
	mgr.CampaignDao.Create(name, price)
	mgr.PikaQGateway.Send(DEFAULT_EXCHANGE, ROUTE_KEY_CONSUMER_ERROR, nil)
	panic("something wrong with pikaq strong")
}
func (mgr *CampaignMgrImpl) CreateWithConsumerErrorPikaQNormal(name string, price *big.Float) {
	mgr.CampaignDao.Create(name, price)
	mgr.PikaQGateway.SendSimple(DEFAULT_EXCHANGE, ROUTE_KEY_CONSUMER_ERROR, nil)
	panic("something wrong with pikaq normal")
}
func (mgr *CampaignMgrImpl) CreateWithConsumerError(name string, price *big.Float) {
	mgr.CampaignDao.Create(name, price)
	mgr.RabbitQGateway.Send(DEFAULT_EXCHANGE, ROUTE_KEY_CONSUMER_ERROR, nil)
	panic("something wrong with rabbitq")
}
func (mgr *CampaignMgrImpl) Update(id int64, price *big.Float) {
	c := mgr.CampaignDao.Get(id)
	if c != nil {
		mgr.CampaignDao.UpdatePriceById(id, price)
		c.Price = price
		mgr.PikaQGateway.SendSimple(DEFAULT_EXCHANGE, ROUTE_KEY2, nil)
	}
}

func TestGetByName(t *testing.T) {
	c := &Campaign{}
	dao := &FakeCampaignDao{getByNameResp: map[string]*Campaign{"x": c}}
	mgr := &CampaignMgrImpl{CampaignDao: dao}
	got := mgr.GetByName("x")
	if got != c {
		t.Errorf("GetByName: expected %p, got %p", c, got)
	}
}
func TestFindAll(t *testing.T) {
	cs := []*Campaign{{}, {}}
	dao := &FakeCampaignDao{findAllResp: cs}
	mgr := &CampaignMgrImpl{CampaignDao: dao}
	got := mgr.FindAll()
	if !reflect.DeepEqual(got, cs) {
		t.Errorf("FindAll: expected %v, got %v", cs, got)
	}
}
func TestCreate(t *testing.T) {
	c := &Campaign{}
	dao := &FakeCampaignDao{createResp: c}
	pikaQ := &FakePikaQGateway{}
	mgr := &CampaignMgrImpl{PikaQGateway: pikaQ, CampaignDao: dao}
	result := mgr.Create("foo", big.NewFloat(19))
	if result != c {
		t.Errorf("Create: expected %p, got %p", c, result)
	}
	args := pikaQ.SendLog.Args
	if !pikaQ.SendLog.Called || args[0] != DEFAULT_EXCHANGE || args[1] != DEFAULT_ROUTE_KEY {
		t.Error("PikaQGateway.Send not called as expected")
	}
}
func TestCreateWithConsumerErrorPikaQStrong(t *testing.T) {
	c := &Campaign{}
	dao := &FakeCampaignDao{createResp: c}
	pikaQ := &FakePikaQGateway{}
	mgr := &CampaignMgrImpl{PikaQGateway: pikaQ, CampaignDao: dao}
	defer func() {
		r := recover()
		if r == nil {
			t.Errorf("Expected panic")
		} else if !containsString(r, "something wrong") {
			t.Errorf("Expected 'something wrong', got %v", r)
		}
	}()
	mgr.CreateWithConsumerErrorPikaQStrong("foo", big.NewFloat(10))
	args := pikaQ.SendLog.Args
	if !pikaQ.SendLog.Called || args[0] != DEFAULT_EXCHANGE || args[1] != ROUTE_KEY_CONSUMER_ERROR {
		t.Error("PikaQGateway.Send for consumer error not called as expected")
	}
}
func TestCreateWithConsumerErrorPikaQNormal(t *testing.T) {
	c := &Campaign{}
	dao := &FakeCampaignDao{createResp: c}
	pikaQ := &FakePikaQGateway{}
	mgr := &CampaignMgrImpl{PikaQGateway: pikaQ, CampaignDao: dao}
	defer func() {
		r := recover()
		if r == nil {
			t.Errorf("Expected panic")
		} else if !containsString(r, "something wrong") {
			t.Errorf("Expected 'something wrong', got %v", r)
		}
	}()
	mgr.CreateWithConsumerErrorPikaQNormal("f", big.NewFloat(1))
	args := pikaQ.SendSimpleLog.Args
	if !pikaQ.SendSimpleLog.Called || args[0] != DEFAULT_EXCHANGE || args[1] != ROUTE_KEY_CONSUMER_ERROR {
		t.Error("PikaQGateway.SendSimple for consumer error not called as expected")
	}
}
func TestCreateWithConsumerError(t *testing.T) {
	c := &Campaign{}
	dao := &FakeCampaignDao{createResp: c}
	rabbit := &FakeRabbitQGateway{}
	mgr := &CampaignMgrImpl{RabbitQGateway: rabbit, CampaignDao: dao}
	defer func() {
		r := recover()
		if r == nil {
			t.Errorf("Expected panic")
		} else if !containsString(r, "something wrong") {
			t.Errorf("Expected 'something wrong', got %v", r)
		}
	}()
	mgr.CreateWithConsumerError("abc", big.NewFloat(0))
	args := rabbit.SendLog.Args
	if !rabbit.SendLog.Called || args[0] != DEFAULT_EXCHANGE || args[1] != ROUTE_KEY_CONSUMER_ERROR {
		t.Error("RabbitQGateway.Send for consumer error not called as expected")
	}
}
func TestUpdate_found(t *testing.T) {
	c := &Campaign{}
	dao := &FakeCampaignDao{getResp: map[int64]*Campaign{22: c}, updatePrice: map[int64]*big.Float{}}
	pikaQ := &FakePikaQGateway{}
	mgr := &CampaignMgrImpl{PikaQGateway: pikaQ, CampaignDao: dao}
	mgr.Update(22, big.NewFloat(33))
	if dao.updatePrice[22].Cmp(big.NewFloat(33)) != 0 {
		t.Errorf("UpdatePriceById not called with expected price: got %v", dao.updatePrice[22])
	}
	if c.Price.Cmp(big.NewFloat(33)) != 0 {
		t.Errorf("Campaign.Price: got %s, want 33", c.Price.String())
	}
	args := pikaQ.SendSimpleLog.Args
	if !pikaQ.SendSimpleLog.Called || args[0] != DEFAULT_EXCHANGE || args[1] != ROUTE_KEY2 {
		t.Error("PikaQGateway.SendSimple not called with right params")
	}
}
func TestUpdate_notFound(t *testing.T) {
	dao := &FakeCampaignDao{getResp: map[int64]*Campaign{}}
	pikaQ := &FakePikaQGateway{}
	mgr := &CampaignMgrImpl{PikaQGateway: pikaQ, CampaignDao: dao}
	mgr.Update(33, big.NewFloat(12))
	if pikaQ.SendSimpleLog.Called {
		t.Error("PikaQGateway.SendSimple called but should not have been")
	}
	if v, ok := dao.updatePrice[33]; ok && v != nil {
		t.Error("UpdatePriceById should not have been called")
	}
}

func containsString(v interface{}, substr string) bool {
	s, ok := v.(string)
	if !ok {
		return false
	}
	return stringContains(s, substr)
}
func stringContains(s, substr string) bool {
	return len(s) >= len(substr) && (s == substr || contains(s, substr))
}
func contains(s, substr string) bool {
	for i := 0; i+len(substr) <= len(s); i++ {
		if s[i:i+len(substr)] == substr {
			return true
		}
	}
	return false
}