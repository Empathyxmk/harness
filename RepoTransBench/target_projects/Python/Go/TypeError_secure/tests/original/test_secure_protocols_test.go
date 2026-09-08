package original

import (
	"TypeError_secure/secure"
	"testing"
)

type DummyHeadersObj struct {
	Headers map[string]string
}
type DummySetHeaderObj struct {
	Called    bool
	LastKey   string
	LastValue string
}
func (d *DummySetHeaderObj) SetHeader(key, value string) {
	d.Called = true
	d.LastKey = key
	d.LastValue = value
}

func TestHeadersProtocolPEP544(t *testing.T) {
	o := DummyHeadersObj{Headers: make(map[string]string)}
	if _, ok := interface{}(o).(secure.HeadersProtocol); !ok {
		t.Errorf("Expected DummyHeadersObj to implement HeadersProtocol")
	}
	var notHdrs interface{} = struct{}{}
	if _, ok := notHdrs.(secure.HeadersProtocol); ok {
		t.Errorf("Expected notHdrs to NOT implement HeadersProtocol")
	}
}

func TestSetHeaderProtocolPEP544(t *testing.T) {
	o := &DummySetHeaderObj{}
	if _, ok := interface{}(o).(secure.SetHeaderProtocol); !ok {
		t.Errorf("Expected DummySetHeaderObj to implement SetHeaderProtocol")
	}
	var notSet interface{} = struct{}{}
	if _, ok := notSet.(secure.SetHeaderProtocol); ok {
		t.Errorf("Expected notSet to NOT implement SetHeaderProtocol")
	}
}

func TestSecureResponseProtocolHeaders(t *testing.T) {
	c := secure.NewCacheControl().NoStore()
	s := secure.NewSecureWithCache(c)
	dummyResp := DummyHeadersObj{Headers: make(map[string]string)}
	if s.HeadersList() == nil || len(s.HeadersList()) == 0 {
		t.Errorf("Expected headers_list present and non-empty")
	}
	if _, ok := s.HeadersList()[0].(*secure.CacheControl); !ok {
		t.Errorf("Expected first header to be CacheControl instance")
	}
}