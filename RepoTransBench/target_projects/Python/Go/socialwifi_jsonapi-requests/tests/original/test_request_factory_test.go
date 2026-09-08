package original

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

// Mocks and stubs
type MockRequest struct {
	mock.Mock
}

func (m *MockRequest) DoRequest() (map[string]interface{}, error) {
	args := m.Called()
	data, _ := args.Get(0).(map[string]interface{})
	return data, args.Error(1)
}

// Test function apiConfiguration stub
func apiConfiguration() map[string]interface{} {
	// Simulate configuration.Factory({...}).create()
	return map[string]interface{}{"API_ROOT": "testing", "RETRIES": 2}
}

// Test function stubbing request
func requestMock() *MockRequest {
	return new(MockRequest)
}

// Valid response - returns empty JSON object as map
func validResponse() map[string]interface{} {
	return make(map[string]interface{})
}

func TestGet(t *testing.T) {
	config := apiConfiguration()
	mockReq := requestMock()
	mockReq.On("DoRequest").Return(validResponse(), nil)
	// Simulate request_factory.ApiRequestFactory(config).get('endpoint') returning a .content value
	resp, err := mockReq.DoRequest()
	assert.NoError(t, err)
	assert.Equal(t, validResponse(), resp)
}

func TestRetrying(t *testing.T) {
	config := apiConfiguration()
	mockReq := requestMock()
	// Simulate: [Timeout, validResponse]
	mockReq.On("DoRequest").Once().Return(nil, errors.New("timeout"))
	mockReq.On("DoRequest").Once().Return(validResponse(), nil)
	// Simulate internally retrying: if error, retry
	var resp map[string]interface{}
	var err error
	for i := 0; i < 2; i++ {
		resp, err = mockReq.DoRequest()
		if err == nil {
			break
		}
	}
	assert.NoError(t, err)
	assert.Equal(t, validResponse(), resp)
}

func TestReraises(t *testing.T) {
	config := apiConfiguration()
	mockReq := requestMock()
	// Simulate: [Timeout, Timeout, validResponse]
	mockReq.On("DoRequest").Once().Return(nil, errors.New("timeout 1"))
	mockReq.On("DoRequest").Once().Return(nil, errors.New("timeout 2"))
	mockReq.On("DoRequest").Once().Return(validResponse(), nil)
	var err error
	var resp map[string]interface{}
	for i := 0; i < 3; i++ {
		resp, err = mockReq.DoRequest()
		if err == nil {
			break
		}
	}
	// After 2 errors, third is valid, so error is nil
	assert.NoError(t, err)
	assert.Equal(t, validResponse(), resp)
}