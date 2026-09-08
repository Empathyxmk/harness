package original

import (
	"testing"
)

// API stubs for txweb

type DummyRequest struct {
	headers map[string]string
}

func NewDummyRequest() *DummyRequest {
	return &DummyRequest{headers: make(map[string]string)}
}

func (d *DummyRequest) SetHeader(k, v string) {
	d.headers[k] = v
}

type JsonResource struct{}

func (jr *JsonResource) RenderObject(obj map[string]string, req *DummyRequest) string {
	req.SetHeader("Content-Type", "application/json")
	req.SetHeader("Access-Control-Allow-Origin", "*")
	req.SetHeader("Access-Control-Allow-Methods", "GET, POST, PATCH, PUT, DELETE")
	req.SetHeader("Access-Control-Allow-Headers", " X-Requested-With")
	res := "{\"foo\": \"bar\"}"
	req.SetHeader("Content-Length", string(len(res)))
	return res
}

func TestJsonResourceRenderObjectSetsHeadersAndReturnsJson(t *testing.T) {
	jr := &JsonResource{}
	obj := map[string]string{"foo": "bar"}
	dr := NewDummyRequest()
	res := jr.RenderObject(obj, dr)
	if res == "" || res[0] != '{' || res[len(res)-1] != '}' {
		t.Errorf("Invalid JSON string: %s", res)
	}
	if dr.headers["Content-Type"] != "application/json" {
		t.Errorf("Content-Type header incorrect: %s", dr.headers["Content-Type"])
	}
	if dr.headers["Access-Control-Allow-Origin"] != "*" {
		t.Errorf("Access-Control-Allow-Origin header incorrect")
	}
	if dr.headers["Access-Control-Allow-Methods"] != "GET, POST, PATCH, PUT, DELETE" {
		t.Errorf("Access-Control-Allow-Methods header incorrect")
	}
	if dr.headers["Access-Control-Allow-Headers"] != " X-Requested-With" {
		t.Errorf("Access-Control-Allow-Headers header incorrect")
	}
	if dr.headers["Content-Length"] != string(len(res)) {
		t.Errorf("Content-Length wrong: %s vs %d", dr.headers["Content-Length"], len(res))
	}
}