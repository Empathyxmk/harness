package public_tests

import (
	"testing"
	"newbeginning6subdir/org/example"
)

func TestHttpResponseShapePublic(t *testing.T) {
	url := "http://example.invalid"
	cookie := "mycookie=12345"
	ua := "PublicAgent/2.0"
	xHeaders := "X-Test: public\nTest-Header: 42"
	method := "get"
	dataBody := ""
	enctypeBody := "application/json"
	follow := false

	resp, err := example.HttpResponse(url, cookie, ua, xHeaders, method, dataBody, enctypeBody, follow)
	if err != nil {
		t.Fatalf("HttpResponse threw: %v", err)
	}
	if resp == nil {
		t.Fatalf("HttpResponse returned nil")
	}
	if len(resp) < 4 {
		t.Errorf("HttpResponse returned too few items: got %d", len(resp))
	}
}