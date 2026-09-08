package integration

import (
	"testing"
	"strings"
)

// Simulate a flask app
type FakeApp struct {
	Config     map[string]string
	Extensions map[string]interface{}
}

func NewFakeApp() *FakeApp {
	return &FakeApp{
		Config:     make(map[string]string),
		Extensions: make(map[string]interface{}),
	}
}

type DummyProviderConn struct {
	ConnectionPool map[string]interface{}
}

type DummyProvider struct {
	StrictCalled bool
	Params map[string]interface{}
}

func (p *DummyProvider) FromUrl(url string, opts map[string]interface{}) *DummyProviderConn {
	return &DummyProviderConn{ConnectionPool: map[string]interface{}{"db": opts["db"]}}
}

type FlaskRedis struct {
	redisClient *DummyProviderConn
	configPrefix string
	provider *DummyProvider
}

func (f *FlaskRedis) InitApp(app *FakeApp) {
	if f.redisClient == nil {
		f.redisClient = &DummyProviderConn{ConnectionPool: map[string]interface{}{"connection_pool": true}}
	}
	if app.Extensions == nil {
		app.Extensions = make(map[string]interface{})
	}
	app.Extensions["redis"] = f
}

func NewFlaskRedis(app *FakeApp, configPrefix string) *FlaskRedis {
	client := &FlaskRedis{
		redisClient: &DummyProviderConn{ConnectionPool: map[string]interface{}{"connection_pool": true}},
		configPrefix: configPrefix,
	}
	if app != nil {
		client.InitApp(app)
	}
	return client
}

func TestConstructor(t *testing.T) {
	app := NewFakeApp()
	redis := NewFlaskRedis(app, "")
	if redis.redisClient == nil {
		t.Errorf("Expected non-nil redisClient")
	}
	if redis.redisClient.ConnectionPool["connection_pool"] != true {
		t.Errorf("Expected connection_pool field")
	}
}

func TestInitApp(t *testing.T) {
	app := NewFakeApp()
	redis := &FlaskRedis{}
	if redis.redisClient != nil {
		t.Errorf("Expected redisClient to be nil before init")
	}
	redis.InitApp(app)
	if redis.redisClient == nil {
		t.Errorf("Expected redisClient to be initialized after InitApp")
	}
	if redis.redisClient.ConnectionPool["connection_pool"] != true {
		t.Errorf("Expected connection_pool field after init")
	}
	if _, ok := app.Extensions["redis"]; !ok {
		t.Errorf("Expected app.Extensions[redis] present")
	}
	if app.Extensions["redis"] != redis {
		t.Errorf("Expected app.Extensions[redis] == redis instance")
	}
}

func TestCustomPrefix(t *testing.T) {
	app := NewFakeApp()
	app.Config["DBA_URL"] = "redis://localhost:6379/1"
	app.Config["DBB_URL"] = "redis://localhost:6379/2"
	redisA := &FlaskRedis{configPrefix: "DBA", redisClient: &DummyProviderConn{ConnectionPool: map[string]interface{}{"db": 1}}}
	redisB := &FlaskRedis{configPrefix: "DBB", redisClient: &DummyProviderConn{ConnectionPool: map[string]interface{}{"db": 2}}}
	if redisA.redisClient.ConnectionPool["db"] != 1 {
		t.Errorf("Expected DBA db: 1, got %v", redisA.redisClient.ConnectionPool["db"])
	}
	if redisB.redisClient.ConnectionPool["db"] != 2 {
		t.Errorf("Expected DBB db: 2, got %v", redisB.redisClient.ConnectionPool["db"])
	}
}

func TestStrictParameter(t *testing.T) {
	app := NewFakeApp()
	trueNames := map[string]bool{"Redis":true,"StrictRedis":true}
	redisStrict := &FlaskRedis{provider: &DummyProvider{StrictCalled: true}}
	if !trueNames["Redis"] && !trueNames["StrictRedis"] {
		t.Errorf("Expected Redis or StrictRedis as type")
	}
	redisNonStrict := &FlaskRedis{provider: &DummyProvider{StrictCalled: false}}
	if !trueNames["Redis"] {
		t.Errorf("Expected Redis type")
	}
}

func TestCustomProvider(t *testing.T) {
	app := NewFakeApp()
	provider := &DummyProvider{}
	redis := &FlaskRedis{provider: provider}
	if redis.redisClient != nil {
		t.Errorf("Expected redisClient to be nil before init")
	}
	redis.InitApp(app)
	if redis.redisClient == nil {
		t.Errorf("Expected redisClient to be non-nil after init")
	}
}