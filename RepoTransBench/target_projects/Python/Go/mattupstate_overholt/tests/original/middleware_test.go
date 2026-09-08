package original

import (
	"testing"
	"bytes"
	"strings"
	"reflect"
	"mattupstate_overholt/overholt/middleware"
)

// DummyApp in Go, simulating WSGI app interface.
type DummyApp struct {
	LastEnviron      map[string]interface{}
	LastStartStatus  string
	LastStartHeaders [][2]string
}

func (d *DummyApp) ServeHTTP(environ map[string]interface{}, startResponse func(string, [][2]string)) [][]byte {
	d.LastEnviron = environ
	startResponse("200 OK", [][2]string{{"Content-Type", "text/plain"}})
	return [][]byte{[]byte("response")}
}

func makeEnviron(method string, queryString string, headers map[string]string) map[string]interface{} {
	environ := map[string]interface{}{
		"REQUEST_METHOD": method,
		"QUERY_STRING":   queryString,
	}
	for k, v := range headers {
		environ[k] = v
	}
	return environ
}

// Emulates middleware function in Go, assumes similar interface. You must have an implementation matching API.
func TestMethodOverrideHeader(t *testing.T) {
	app := &DummyApp{}
	mw := middleware.NewHTTPMethodOverrideMiddleware(app, "", "", []string{})
	environ := makeEnviron("POST", "", map[string]string{"HTTP_X_HTTP_METHOD_OVERRIDE": "DELETE"})
	called := struct {
		status  string
		headers [][2]string
	}{}
	startResponse := func(status string, headers [][2]string) {
		called.status = status
		called.headers = headers
	}
	result := mw.ServeHTTP(environ, startResponse)
	// In Go: let's assume the middleware modifies REQUEST_METHOD as needed
	if rm, ok := app.LastEnviron["REQUEST_METHOD"]; ok {
		// We expect middleware to override to "DELETE" (as []byte or string)
		switch v := rm.(type) {
		case string:
			if v != "DELETE" {
				t.Errorf("Expected overridden REQUEST_METHOD 'DELETE', got '%v'", v)
			}
		default:
			t.Errorf("REQUEST_METHOD has unexpected type %T", v)
		}
	} else {
		t.Errorf("REQUEST_METHOD missing from environ")
	}
	// We don't have Content-Length in our dummy implementation, but assert result and status
	if !reflect.DeepEqual(result, [][]byte{[]byte("response")}) {
		t.Errorf("Incorrect result: got %v", result)
	}
	if called.status != "200 OK" {
		t.Errorf("Expected status 200 OK, got %s", called.status)
	}
}

func TestMethodOverrideQuerystring(t *testing.T) {
	app := &DummyApp{}
	mw := middleware.NewHTTPMethodOverrideMiddleware(app, "", "", []string{})
	environ := makeEnviron("POST", "foo=bar&__METHOD__=PUT", map[string]string{})
	called := struct {
		status  string
		headers [][2]string
	}{}
	startResponse := func(status string, headers [][2]string) {
		called.status = status
		called.headers = headers
	}
	result := mw.ServeHTTP(environ, startResponse)
	if rm, ok := app.LastEnviron["REQUEST_METHOD"]; ok {
		switch v := rm.(type) {
		case string:
			if v != "PUT" {
				t.Errorf("Expected overridden REQUEST_METHOD 'PUT', got '%v'", v)
			}
		default:
			t.Errorf("REQUEST_METHOD has unexpected type %T", v)
		}
	} else {
		t.Errorf("REQUEST_METHOD missing from environ")
	}
	if !reflect.DeepEqual(result, [][]byte{[]byte("response")}) {
		t.Errorf("Incorrect result: got %v", result)
	}
}

func TestNoOverride(t *testing.T) {
	app := &DummyApp{}
	mw := middleware.NewHTTPMethodOverrideMiddleware(app, "", "", []string{})
	environ := makeEnviron("GET", "", map[string]string{})
	called := struct {
		status  string
		headers [][2]string
	}{}
	startResponse := func(status string, headers [][2]string) {
		called.status = status
		called.headers = headers
	}
	result := mw.ServeHTTP(environ, startResponse)
	if rm, ok := app.LastEnviron["REQUEST_METHOD"]; ok {
		if rm != "GET" {
			t.Errorf("Expected REQUEST_METHOD 'GET', got '%v'", rm)
		}
	} else {
		t.Errorf("REQUEST_METHOD missing from environ")
	}
	if !reflect.DeepEqual(result, [][]byte{[]byte("response")}) {
		t.Errorf("Incorrect result: got %v", result)
	}
}

func TestOverrideWithCustom(t *testing.T) {
	app := &DummyApp{}
	mw := middleware.NewHTTPMethodOverrideMiddleware(app, "X-MY-HEADER", "__MY_METHOD__", []string{"PUT"})
	environ := makeEnviron("POST", "", map[string]string{"HTTP_X_MY_HEADER": "PUT"})
	called := struct {
		status  string
		headers [][2]string
	}{}
	startResponse := func(status string, headers [][2]string) {
		called.status = status
		called.headers = headers
	}
	result := mw.ServeHTTP(environ, startResponse)
	if rm, ok := app.LastEnviron["REQUEST_METHOD"]; ok {
		if rm != "PUT" {
			t.Errorf("Expected overridden REQUEST_METHOD 'PUT', got '%v'", rm)
		}
	} else {
		t.Errorf("REQUEST_METHOD missing from environ")
	}
	if !reflect.DeepEqual(result, [][]byte{[]byte("response")}) {
		t.Errorf("Incorrect result: got %v", result)
	}
}

func TestOverrideNotAllowed(t *testing.T) {
	app := &DummyApp{}
	mw := middleware.NewHTTPMethodOverrideMiddleware(app, "", "", []string{"POST"})
	environ := makeEnviron("POST", "", map[string]string{"HTTP_X_HTTP_METHOD_OVERRIDE": "PATCH"})
	called := struct {
		status  string
		headers [][2]string
	}{}
	startResponse := func(status string, headers [][2]string) {
		called.status = status
		called.headers = headers
	}
	result := mw.ServeHTTP(environ, startResponse)
	if rm, ok := app.LastEnviron["REQUEST_METHOD"]; ok {
		if rm != "POST" {
			t.Errorf("Expected REQUEST_METHOD to stay 'POST', got '%v'", rm)
		}
	} else {
		t.Errorf("REQUEST_METHOD missing from environ")
	}
	if !reflect.DeepEqual(result, [][]byte{[]byte("response")}) {
		t.Errorf("Incorrect result: got %v", result)
	}
}

func TestGetFromQuerystringReturnsNone(t *testing.T) {
	app := &DummyApp{}
	mw := middleware.NewHTTPMethodOverrideMiddleware(app, "", "", []string{})
	environ := makeEnviron("POST", "foo=bar", map[string]string{})
	method := mw.GetFromQuerystring(environ)
	if method != "" {
		t.Errorf("Expected no override from querystring, got %v", method)
	}
}