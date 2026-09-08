package public_tests

import "testing"

type pyzbar struct{}

func (p *pyzbar) Version() string  { return "1.0.1" }
func (p *pyzbar) Doc() string      { return "docstring" }

func TestInitPublic(t *testing.T) {
	p := &pyzbar{}
	if p.Doc() == "" {
		t.Errorf("Expected docstring")
	}
	if p.Version() == "" {
		t.Errorf("Expected version attribute")
	}
}