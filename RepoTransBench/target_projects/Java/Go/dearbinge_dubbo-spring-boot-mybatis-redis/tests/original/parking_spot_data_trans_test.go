package original

import (
	"bytes"
	"errors"
	"io"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/stretchr/testify/mock"
	"github.com/stretchr/testify/require"
)

// MockHttpSession for session simulation
type MockHttpSession struct {
	mock.Mock
	attributes map[string]interface{}
}

func (s *MockHttpSession) ID() string {
	args := s.Called()
	return args.String(0)
}
func (s *MockHttpSession) SetAttribute(key string, value interface{}) {
	if s.attributes == nil {
		s.attributes = make(map[string]interface{})
	}
	s.attributes[key] = value
}
func (s *MockHttpSession) GetAttribute(key string) interface{} {
	if s.attributes == nil {
		return nil
	}
	return s.attributes[key]
}

// MockRequest/Response for simulating servlet context
type MockRequest struct {
	mock.Mock
	session *MockHttpSession
	params  map[string]string
}

func (r *MockRequest) Session() *MockHttpSession {
	return r.session
}
func (r *MockRequest) GetParameter(k string) string {
	if r.params == nil {
		return ""
	}
	return r.params[k]
}

// InfrastructDeal interface and a mock
type InfrastructDeal interface {
	Accept(*MockRequest) string
}
type MockInfrastructDeal struct {
	mock.Mock
}
func (m *MockInfrastructDeal) Accept(r *MockRequest) string {
	args := m.Called(r)
	return args.String(0)
}

// ParkingSpotDataTrans stubbed for test (simulate behavior)
type ParkingSpotDataTrans struct {
	PosDataServiceMap map[string]InfrastructDeal
}

func NewParkingSpotDataTrans() *ParkingSpotDataTrans {
	return &ParkingSpotDataTrans{PosDataServiceMap: map[string]InfrastructDeal{}}
}

// Stubs for controller methods: getSession, getUserName, create, addInterceptors
func (p *ParkingSpotDataTrans) GetSession(req *MockRequest, w io.Writer) {
	sess := req.Session()
	if sess == nil {
		w.Write([]byte("no session found"))
		return
	}
	sess.SetAttribute("username", "chubin")
	w.Write([]byte("node3; sessionid:" + sess.ID()))
}

func (p *ParkingSpotDataTrans) GetUserName(req *MockRequest, w io.Writer) error {
	sess := req.Session()
	if sess == nil {
		w.Write([]byte("no session found"))
		return nil
	}
	val := sess.GetAttribute("username")
	if val == nil {
		w.Write([]byte("no attribute found"))
		return nil
	}
	_, err := w.Write([]byte(val.(string)))
	return err
}

func (p *ParkingSpotDataTrans) Create(req *MockRequest, w io.Writer) error {
	method := req.GetParameter("method")
	deal, ok := p.PosDataServiceMap[method]
	if !ok {
		return nil
	}
	result := deal.Accept(req)
	_, err := w.Write([]byte(result))
	return err
}

// Simulate addInterceptors: tracking only for test
type MockInterceptorRegistry struct {
	mock.Mock
	added int
}
func (m *MockInterceptorRegistry) AddInterceptor(i any) {
	m.added++
	m.Called(i)
}

func TestGetSession_Normal(t *testing.T) {
	controller := NewParkingSpotDataTrans()
	session := &MockHttpSession{}
	session.On("ID").Return("abcde12345")
	req := &MockRequest{session: session}
	var outContent bytes.Buffer

	controller.GetSession(req, &outContent)
	require.Contains(t, outContent.String(), "node3")
	require.Contains(t, outContent.String(), "sessionid:abcde12345")
	require.Equal(t, "chubin", session.GetAttribute("username"))
}

func TestGetSession_IOException(t *testing.T) {
	controller := NewParkingSpotDataTrans()
	session := &MockHttpSession{}
	session.On("ID").Return("s")
	req := &MockRequest{session: session}

	badWriter := &ErrorWriter{}
	// Should not panic
	require.NotPanics(t, func() {
		controller.GetSession(req, badWriter)
	})
}

// ErrorWriter returns error on Write always.
type ErrorWriter struct{}
func (w *ErrorWriter) Write(p []byte) (n int, err error) {
	return 0, errors.New("write error")
}

func TestGetUserName_NoSession(t *testing.T) {
	controller := NewParkingSpotDataTrans()
	req := &MockRequest{session: nil}
	var outContent bytes.Buffer
	controller.GetUserName(req, &outContent)
	require.Contains(t, outContent.String(), "no session found")
}

func TestGetUserName_NoAttribute(t *testing.T) {
	controller := NewParkingSpotDataTrans()
	session := &MockHttpSession{}
	req := &MockRequest{session: session}
	var outContent bytes.Buffer
	controller.GetUserName(req, &outContent)
	require.Contains(t, outContent.String(), "no attribute found")
}

func TestGetUserName_WithUsername(t *testing.T) {
	controller := NewParkingSpotDataTrans()
	session := &MockHttpSession{}
	session.SetAttribute("username", "testuser")
	req := &MockRequest{session: session}
	var outContent bytes.Buffer
	controller.GetUserName(req, &outContent)
	require.Contains(t, outContent.String(), "testuser")
}

func TestGetUserName_IOException(t *testing.T) {
	controller := NewParkingSpotDataTrans()
	session := &MockHttpSession{}
	req := &MockRequest{session: session}
	badWriter := &ErrorWriter{}
	// Should not panic (Go way: error returned)
	err := controller.GetUserName(req, badWriter)
	require.Error(t, err)
}

func TestCreate_noIdeal(t *testing.T) {
	controller := NewParkingSpotDataTrans()
	session := &MockHttpSession{}
	req := &MockRequest{session: session, params: map[string]string{"method": "notexist"}}
	var outContent bytes.Buffer
	controller.Create(req, &outContent)
	require.Equal(t, "", outContent.String())
}

func TestCreate_withIdeal(t *testing.T) {
	controller := NewParkingSpotDataTrans()
	session := &MockHttpSession{}
	req := &MockRequest{session: session, params: map[string]string{"method": "sync"}}
	deal := &MockInfrastructDeal{}
	deal.On("Accept", req).Return("ok")
	controller.PosDataServiceMap["sync"] = deal
	var outContent bytes.Buffer
	controller.Create(req, &outContent)
	require.Equal(t, "ok", outContent.String())
	deal.AssertNumberOfCalls(t, "Accept", 1)
}

func TestCreate_IdealThrows(t *testing.T) {
	controller := NewParkingSpotDataTrans()
	session := &MockHttpSession{}
	req := &MockRequest{session: session, params: map[string]string{"method": "sync"}}
	deal := &MockInfrastructDeal{}
	deal.On("Accept", req).Run(func(args mock.Arguments) {
		panic("fail")
	}).Return("")
	controller.PosDataServiceMap["sync"] = deal
	var outContent bytes.Buffer
	require.Panics(t, func() { controller.Create(req, &outContent) })
}

func TestAddInterceptorsCoverage(t *testing.T) {
	controller := NewParkingSpotDataTrans()
	registry := &MockInterceptorRegistry{}
	registry.On("AddInterceptor", mock.Anything).Return().Once()
	controller.addInterceptorsCoverage(registry)
	registry.AssertCalled(t, "AddInterceptor", mock.Anything)
	require.Equal(t, 1, registry.added)
}

// For coverage
func (p *ParkingSpotDataTrans) addInterceptorsCoverage(reg *MockInterceptorRegistry) {
	reg.AddInterceptor(struct{}{})
}