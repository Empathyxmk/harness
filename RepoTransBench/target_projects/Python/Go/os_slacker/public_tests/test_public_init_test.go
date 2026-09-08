package public_tests

import (
	"encoding/json"
	"testing"
	"time"

	"github.com/jarcoal/httpmock"
	"github.com/stretchr/testify/assert"
)

// Stubs for API types and functions for illustration only.
// Replace these with real implementations in production.
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

type Error struct{ Msg string }
func (e Error) Error() string { return e.Msg }

type BaseAPI struct {
	Token            string
	RateLimitRetries int
	Session          interface{}
}

func (api *BaseAPI) Get(endpoint string) *Response {
	resp, err := httpmock.Get("https://slack.com/api/" + endpoint)
	if err != nil {
		return &Response{Successful: false, ErrorStr: err.Error()}
	}
	return NewResponse(resp.Body)
}
func (api *BaseAPI) _session_get(url string, params map[string]interface{}) {}
func (api *BaseAPI) _session_post(url string, data map[string]interface{}) {}

type API struct{ BaseAPI }
func (api *API) Test(params ...interface{}) {}

type Auth struct{ BaseAPI }
func (a *Auth) Test()                   {}
func (a *Auth) Revoke(opts ...interface{}) {}

func TestResponsePublic_SuccessfulResponse(t *testing.T) {
	body := `{"ok": true, "value": 100}`
	resp := NewResponse(body)
	assert.True(t, resp.Successful)
	assert.Equal(t, float64(100), resp.Body["value"])
	assert.Equal(t, "", resp.ErrorStr)
	assert.Contains(t, resp.String(), `"value":100`)
}

func TestResponsePublic_ErrorResponse(t *testing.T) {
	body := `{"ok": false, "error": "otherfail"}`
	resp := NewResponse(body)
	assert.False(t, resp.Successful)
	assert.Equal(t, "otherfail", resp.ErrorStr)
	assert.Contains(t, resp.String(), "otherfail")
}

func TestBaseAPIPublic_GetSuccess(t *testing.T) {
	httpmock.Activate()
	defer httpmock.DeactivateAndReset()
	httpmock.RegisterResponder("GET", "https://slack.com/api/api.other_test",
		httpmock.NewStringResponder(200, `{"ok": true, "x": 5}`),
	)
	api := &BaseAPI{Token: "another_test"}
	resp := api.Get("api.other_test")
	assert.True(t, resp.Successful)
}

func TestBaseAPIPublic_GetError(t *testing.T) {
	httpmock.Activate()
	defer httpmock.DeactivateAndReset()
	httpmock.RegisterResponder("GET", "https://slack.com/api/api.other_test",
		httpmock.NewStringResponder(200, `{"ok": false, "error":"badrequest"}`),
	)
	api := &BaseAPI{Token: "another_test"}
	resp := api.Get("api.other_test")
	assert.False(t, resp.Successful)
	assert.Equal(t, "badrequest", resp.ErrorStr)
}

func TestBaseAPIPublic_Get429Retry(t *testing.T) {
	httpmock.Activate()
	defer httpmock.DeactivateAndReset()
	callCount := 0
	httpmock.RegisterResponder("GET", "https://slack.com/api/api.other_test",
		func(req *httpmock.Request) (*httpmock.Response, error) {
			if callCount == 0 {
				callCount++
				resp := httpmock.NewBytesResponse(429, []byte{})
				resp.Header.Set("retry-after", "1")
				return resp, nil
			}
			return httpmock.NewStringResponse(200, `{"ok": true}`), nil
		})
	api := &BaseAPI{Token: "another_test", RateLimitRetries: 2}
	oldSleep := time.Sleep
	defer func() { time.Sleep = oldSleep }()
	time.Sleep = func(d time.Duration) {}
	resp := api.Get("api.other_test")
	assert.True(t, resp.Successful)
}

func TestAPIPublic_TestMethod(t *testing.T) {
	api := &API{BaseAPI{Token: "T_public"}}
	api.Test()
	api.Test("badrequest", 42)
}

func TestAuthPublic_Test(t *testing.T) {
	a := &Auth{BaseAPI{Token: "T_public"}}
	a.Test()
}

func TestAuthPublic_Revoke(t *testing.T) {
	a := &Auth{BaseAPI{Token: "T_public"}}
	a.Revoke()
	a.Revoke(false)
}

func TestErrorPublic_ErrorMethod(t *testing.T) {
	e := Error{"another error message"}
	assert.Equal(t, "another error message", e.Error())
}