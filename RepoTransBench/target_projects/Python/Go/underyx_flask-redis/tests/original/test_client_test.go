package original

import (
	"testing"
	"github.com/stretchr/testify/mock"
)

// A minimal mock of FlaskRedis for constructor test
type MockFlaskRedis struct {
	mock.Mock
	app interface{}
}

func (m *MockFlaskRedis) InitApp(app interface{}) {
	m.Called(app)
}

func TestConstructorApp(t *testing.T) {
	mockFlaskRedis := new(MockFlaskRedis)
	appStub := struct{}{}
	mockFlaskRedis.On("InitApp", appStub).Return()
	mockFlaskRedis.InitApp(appStub)
	mockFlaskRedis.AssertCalled(t, "InitApp", appStub)
}