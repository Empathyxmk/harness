package public_tests

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

// Test function apiConfiguration stub (public variant)
func apiConfigurationPublic() map[string]interface{} {
	// Simulate configuration.Factory({...}).create()
	return map[string]interface{}{"API_ROOT": "mockapi", "RETRIES": 3}
}

// Test function stubbing request
func requestMockPublic() *MockRequest {
	return new(MockRequest)
}

// Valid response - returns created message
func validResponsePublic() map[string]interface{} {
	return map[string]interface{}{"message": "created"}
}

func TestGetPublic(t *testing.T) {
	config := apiConfigurationPublic()
	mockReq := requestMockPublic()
	mockReq.On("DoRequest").Return(validResponsePublic(), nil)
	resp, err := mockReq.DoRequest()
	assert.NoError(t, err)
	assert.Equal(t, validResponsePublic(), resp)
}

func TestRetryingPublic(t *testing.T) {
	config := apiConfigurationPublic()
	mockReq := requestMockPublic()
	mockReq.On("DoRequest").Once().Return(nil, errors.New("timeout"))
	mockReq.On("DoRequest").Once().Return(nil, errors.New("timeout"))
	mockReq.On("DoRequest").Once().Return(validResponsePublic(), nil)
	var resp map[string]interface{}
	var err error
	for i := 0; i < 3; i++ {
		resp, err = mockReq.DoRequest()
		if err == nil {
			break
		}
	}
	assert.NoError(t, err)
	assert.Equal(t, validResponsePublic(), resp)
}

func TestReraisesPublic(t *testing.T) {
	config := apiConfigurationPublic()
	mockReq := requestMockPublic()
	mockReq.On("DoRequest").Once().Return(nil, errors.New("timeout"))
	mockReq.On("DoRequest").Once().Return(nil, errors.New("timeout"))
	mockReq.On("DoRequest").Once().Return(nil, errors.New("timeout"))
	mockReq.On("DoRequest").Once().Return(validResponsePublic(), nil)
	var err error
	var resp map[string]interface{}
	for i := 0; i < 4; i++ {
		resp, err = mockReq.DoRequest()
		if err == nil {
			break
		}
	}
	if err == nil {
		t.Fatal("expected error was not raised")
	}
}