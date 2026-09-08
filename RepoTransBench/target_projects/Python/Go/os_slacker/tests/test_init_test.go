package tests

import (
	"encoding/json"
	"errors"
	"testing"
	"time"

	"github.com/jarcoal/httpmock"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

// Stubs for os_slacker internal types so tests compile.
// Replace with real implementations when porting production code.
type Response struct {
	Body       map[string]interface{}
	Successful bool
	ErrorStr   string
}

func NewResponse(body string) *Response {
	var m map[string]interface{}
	_ = json.Unmarshal([]byte(body), &m)
	successful := false
	errStr := ""
	if v, ok := m["ok"]; ok && v == true {
		successful = true
	}
	if v, ok := m["error"]; ok {
		errStr, _ = v.(string)
	}
	return &Response{Body: m, Successful: successful, ErrorStr: errStr}
}

func (r *Response) String() string {
	b, _ := json.Marshal(r.Body)
	return string(b)
}

var ErrCustom = errors.New("fail")

type Error struct {
	Msg string
}

func (e Error) Error() string { return e.Msg }

type BaseAPI struct {
	Token            string
	RateLimitRetries int
	Session          interface{}
}

func (api *BaseAPI) Get(endpoint string) *Response {
	// This stub just simulates a basic API call for testing
	resp, err := httpmock.Get("https://slack.com/api/" + endpoint)
	if err != nil {
		return &Response{Successful: false, ErrorStr: err.Error()}
	}
	return NewResponse(resp.Body)
}

func (api *BaseAPI) _session_get(url string, params map[string]interface{}) {
	// Placeholder mock call
}

func (api *BaseAPI) _session_post(url string, data map[string]interface{}) {
	// Placeholder mock call
}

type API struct {
	BaseAPI
}

func (api *API) Test(params ...interface{}) {
	// Simulate API.test() logic.
}

type Auth struct {
	BaseAPI
}

func (a *Auth) Test()           {}
func (a *Auth) Revoke(opts ...interface{}) {}

func TestResponse_SuccessfulResponse(t *testing.T) {
	body := `{"ok": true, "a": 42}`
	resp := NewResponse(body)
	assert.True(t, resp.Successful)
	assert.Equal(t, float64(42), resp.Body["a"])
	assert.Equal(t, "", resp.ErrorStr)
	assert.Contains(t, resp.String(), `"a":42`)
}

func TestResponse_ErrorResponse(t *testing.T) {
	body := `{"ok": false, "error": "fail"}`
	resp := NewResponse(body)
	assert.False(t, resp.Successful)
	assert.Equal(t, "fail", resp.ErrorStr)
	assert.Contains(t, resp.String(), "fail")
}

func TestBaseAPI_GetSuccess(t *testing.T) {
	httpmock.Activate()
	defer httpmock.DeactivateAndReset()
	httpmock.RegisterResponder("GET", "https://slack.com/api/api.test",
		httpmock.NewStringResponder(200, `{"ok": true}`),
	)
	api := &BaseAPI{Token: "test"}
	resp := api.Get("api.test")
	assert.True(t, resp.Successful)
}

func TestBaseAPI_GetError(t *testing.T) {
	httpmock.Activate()
	defer httpmock.DeactivateAndReset()
	httpmock.RegisterResponder("GET", "https://slack.com/api/api.test",
		httpmock.NewStringResponder(200, `{"ok": false, "error":"fail"}`),
	)
	api := &BaseAPI{Token: "test"}
	resp := api.Get("api.test")
	assert.False(t, resp.Successful)
	assert.Equal(t, "fail", resp.ErrorStr)
}

func TestBaseAPI_Get429Retry(t *testing.T) {
	// Simulate 429, then success
	httpmock.Activate()
	defer httpmock.DeactivateAndReset()
	callCount := 0
	httpmock.RegisterResponder("GET", "https://slack.com/api/api.test",
		func(req *httpmock.Request) (*httpmock.Response, error) {
			if callCount == 0 {
				callCount++
				resp := httpmock.NewBytesResponse(429, []byte{})
				resp.Header.Set("retry-after", "0")
				return resp, nil
			}
			return httpmock.NewStringResponse(200, `{"ok": true}`), nil
		})
	api := &BaseAPI{Token: "test", RateLimitRetries: 2}
	// time.Sleep(0) is essentially a no-op
	oldSleep := time.Sleep
	defer func() { time.Sleep = oldSleep }()
	time.Sleep = func(d time.Duration) {}
	resp := api.Get("api.test")
	assert.True(t, resp.Successful)
}

func TestAPI_TestMethod(t *testing.T) {
	// This just ensures the method can be called
	api := &API{BaseAPI{Token: "T"}}
	api.Test()
	api.Test("fail", 1)
}

func TestAuth_Test(t *testing.T) {
	a := &Auth{BaseAPI{Token: "T"}}
	a.Test()
	// Assume this calls BaseAPI.Get("auth.test") as in Python
}

func TestAuth_Revoke(t *testing.T) {
	a := &Auth{BaseAPI{Token: "T"}}
	a.Revoke()
	a.Revoke(false)
}

func TestError_ErrorMethod(t *testing.T) {
	e := Error{"some error"}
	assert.Equal(t, "some error", e.Error())
}