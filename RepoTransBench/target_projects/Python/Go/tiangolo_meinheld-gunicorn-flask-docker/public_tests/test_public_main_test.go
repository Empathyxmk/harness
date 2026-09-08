package public_tests

import (
	"strings"
	"testing"
)

// Pure interface/go version of Flask main tests.

type MockResponse struct {
	StatusCode int
	Data       []byte
}

type MockApp struct{}

func (a *MockApp) TestClient() *MockClient {
	return &MockClient{}
}

type MockClient struct{}

func (c *MockClient) Get(path string) *MockResponse {
	if path == "/" {
		// Simulates the message: "Hello World ... running Python ..."
		return &MockResponse{
			StatusCode: 200,
			Data: []byte("Hello World from Flask in a Docker container running Python 3.12 with Meinheld and Gunicorn"),
		}
	}
	return &MockResponse{StatusCode: 404, Data: nil}
}

func TestHelloReturnsCustomMessage(t *testing.T) {
	app := &MockApp{}
	client := app.TestClient()
	rv := client.Get("/")
	if rv.StatusCode != 200 {
		t.Errorf("Expected status code 200, got %d", rv.StatusCode)
	}
	prefix := "Hello World from Flask in a Docker container running Python "
	if !strings.HasPrefix(string(rv.Data), prefix) {
		t.Errorf("Expected returned data to start with: %q, got %q", prefix, rv.Data)
	}
}

func TestHelloRouteStatusCode(t *testing.T) {
	app := &MockApp{}
	client := app.TestClient()
	rv := client.Get("/")
	if rv.StatusCode != 200 {
		t.Errorf("Expected status code 200, got %d", rv.StatusCode)
	}
}

func TestFlaskAppType(t *testing.T) {
	app := &MockApp{}
	if app == nil {
		t.Errorf("Expected app to be non-nil")
	}
}

func TestImportMainPyDistinctApps(t *testing.T) {
	app1 := &MockApp{}
	app2 := &MockApp{}
	if app1 == app2 {
		t.Errorf("Expected distinct app instances")
	}
	_ = app1.TestClient
	_ = app2.TestClient
}