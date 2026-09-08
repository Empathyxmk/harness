package public_tests

import (
	"TypeError_secure/secure"
	"testing"
)

type AlternateHeadersObj struct {
	Headers map[string]string
}
type AlternateSetHeaderObj struct {
	WasCalled bool
	K         string
	V         string
}
func (a *AlternateSetHeaderObj) SetHeader(k, v string) {
	a.WasCalled = true
	a.K = k
	a.V = v
}

func TestHeadersProtocolPublic(t *testing.T) {
	o := AlternateHeadersObj{Headers: map[string]string{"X-Test": "abc"}}
	if _, ok := interface{}(o).(secure.HeadersProtocol); !ok {
		t.Errorf("Expected AlternateHeadersObj to implement HeadersProtocol")
	}
	var notHdrs interface{} = 42
	if _, ok := notHdrs.(secure.HeadersProtocol); ok {
		t.Errorf("Did not expect int to implement HeadersProtocol")
	}
}

func TestSetHeaderProtocolPublic(t *testing.T) {
	o := &AlternateSetHeaderObj{}
	if _, ok := interface{}(o).(secure.SetHeaderProtocol); !ok {
		t.Errorf("Expected AlternateSetHeaderObj to implement SetHeaderProtocol")
	}
	var notSet interface{} = []int{}
	if _, ok := notSet.(secure.SetHeaderProtocol); ok {
		t.Errorf("Did not expect slice to implement SetHeaderProtocol")
	}
}

func TestSecureResponseProtocolHeadersPublic(t *testing.T) {
	s := secure.NewSecureWithHSTS(secure.NewStrictTransportSecurity().MaxAge(777))
	dummyResp := AlternateHeadersObj{Headers: map[string]string{}}
	if s.HeadersList() == nil || len(s.HeadersList()) == 0 {
		t.Errorf("Expected headers_list present and non-empty")
	}
	if _, ok := s.HeadersList()[0].(*secure.StrictTransportSecurity); !ok {
		t.Errorf("Expected first header to be StrictTransportSecurity")
	}
}