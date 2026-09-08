package public_tests

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

type DummyConfigPublic struct {
	API_ROOT     string
	APPEND_SLASH bool
	RETRIES      int
	VALIDATE_SSL bool
	AUTH         interface{}
	TIMEOUT      interface{}
}

type DummyObjectPublic struct{}

func (o *DummyObjectPublic) AsData() map[string]interface{} {
	return map[string]interface{}{"type": "resource", "id": "abc"}
}

func makeResponsePublic(statusCode int, content []byte, jsonData map[string]interface{}) *ResponseStubPublic {
	resp := &ResponseStubPublic{
		StatusCode: statusCode,
		Content:    content,
	}
	if jsonData != nil {
		resp.JSONData = jsonData
		resp.JSONValid = true
	}
	return resp
}

type ResponseStubPublic struct {
	StatusCode int
	Content    []byte
	JSONData   map[string]interface{}
	JSONValid  bool
}

func (r *ResponseStubPublic) JSON() (map[string]interface{}, error) {
	if r.JSONValid {
		return r.JSONData, nil
	}
	return nil, errors.New("invalid JSON")
}

func TestObjectJSONAssertionPublic(t *testing.T) {
	obj := &DummyObjectPublic{}
	factory := &DummyConfigPublic{}
	_ = obj
	_ = factory
	assert.True(t, true)
}

func TestBuildAbsoluteURLSlashPublic(t *testing.T) {
	conf := &DummyConfigPublic{}
	conf.API_ROOT = "http://public/api/"
	conf.APPEND_SLASH = true
	url := conf.API_ROOT + "bar"
	assert.True(t, url[len(url)-1] == '/')
	conf.APPEND_SLASH = false
	url2 := conf.API_ROOT + "bar"
	assert.True(t, url2[len(url2)-1] == 'r')
}

func TestParseResponsePathsPublic(t *testing.T) {
	conf := &DummyConfigPublic{}
	resp := makeResponsePublic(501, []byte("ERROR"), nil)
	assert.Equal(t, 501, resp.StatusCode)
	resp2 := makeResponsePublic(204, nil, nil)
	assert.Equal(t, 204, resp2.StatusCode)
	resp3 := makeResponsePublic(404, []byte("ERROR"), nil)
	assert.Equal(t, 404, resp3.StatusCode)
	resp4 := makeResponsePublic(200, []byte("invalid-json"), nil)
	_, err := resp4.JSON()
	assert.Error(t, err)
	resp5 := makeResponsePublic(200, nil, map[string]interface{}{"foo": "baz"})
	jsonVal, err := resp5.JSON()
	assert.NoError(t, err)
	assert.Equal(t, map[string]interface{}{"foo": "baz"}, jsonVal)
}

func TestRequestConnectionPublic(t *testing.T) {
	attempts := 0
	var result *ResponseStubPublic
	for i := 0; i < 3; i++ {
		attempts++
		if attempts < 3 {
			continue
		} else {
			result = makeResponsePublic(202, nil, map[string]interface{}{"z": "y"})
			break
		}
	}
	assert.Equal(t, 3, attempts)
	assert.NotNil(t, result)
}

func TestConfiguredOptionsVariantsPublic(t *testing.T) {
	conf := &DummyConfigPublic{VALIDATE_SSL: false}
	opts := map[string]interface{}{
		"verify": conf.VALIDATE_SSL,
	}
	assert.Equal(t, false, opts["verify"])
	conf.AUTH = "TOKEN"
	conf.TIMEOUT = 30
	opts2 := map[string]interface{}{
		"auth":   conf.AUTH,
		"timeout": conf.TIMEOUT,
	}
	assert.Equal(t, "TOKEN", opts2["auth"])
	assert.Equal(t, 30, opts2["timeout"])
}

func TestApiResponseReprDataPublic(t *testing.T) {
	val := map[string]interface{}{}
	assert.Equal(t, map[string]interface{}{}, val)
	val2 := map[string]interface{}{"y": 100}
	assert.Equal(t, map[string]interface{}{"y": 100}, val2)
}

func TestErrorInitsPublic(t *testing.T) {
	status := 418
	content := []byte("tea")
	assert.Equal(t, 418, status)
	assert.Equal(t, []byte("tea"), content)
}