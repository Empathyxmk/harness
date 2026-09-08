package original

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/mock"
	"github.com/stretchr/testify/require"
)

// ParkingBasicDataSync is a stub for the class under test.
type ParkingBasicDataSync struct{}

func (d *ParkingBasicDataSync) Accept(req *MockHttpRequest) string {
	v, err := req.GetParameter("jsonBody")
	if err != nil {
		return "fail"
	}
	if v != "" {
		return "success: " + v
	}
	return "fail"
}

type MockHttpRequest struct {
	mock.Mock
	params map[string]string
	errs   map[string]error
}

func (r *MockHttpRequest) GetParameter(k string) (string, error) {
	if r.errs != nil {
		if err, ok := r.errs[k]; ok {
			return "", err
		}
	}
	if r.params == nil {
		return "", nil
	}
	return r.params[k], nil
}

func TestAcceptReturnsSuccess(t *testing.T) {
	dataSync := &ParkingBasicDataSync{}
	req := &MockHttpRequest{params: map[string]string{"jsonBody": "{\"key\":\"value\"}"}}
	res := dataSync.Accept(req)
	require.Contains(t, res, "success")
}

func TestAcceptReturnsFail(t *testing.T) {
	dataSync := &ParkingBasicDataSync{}
	req := &MockHttpRequest{params: map[string]string{}}
	res := dataSync.Accept(req)
	require.Contains(t, res, "fail")
}

func TestAcceptExceptionInParameter(t *testing.T) {
	dataSync := &ParkingBasicDataSync{}
	req := &MockHttpRequest{errs: map[string]error{"jsonBody": errors.New("error")}}
	res := dataSync.Accept(req)
	require.Contains(t, res, "fail")
}