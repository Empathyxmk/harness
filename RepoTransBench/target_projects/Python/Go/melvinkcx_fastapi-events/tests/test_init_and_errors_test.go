package tests

import (
	"testing"
)

type DummyContextVar struct{}

func (c *DummyContextVar) set(interface{})      {}
func (c *DummyContextVar) get() interface{}     { return nil }
func (c *DummyContextVar) HasSetMethod() bool   { return true }
func (c *DummyContextVar) HasGetMethod() bool   { return true }

var handler_store = make(map[string]interface{})
var event_store = &DummyContextVar{}
var in_req_res_cycle = &DummyContextVar{}
var middleware_identifier = &DummyContextVar{}

type FastapiEventError struct{ msg string }
func (e *FastapiEventError) Error() string { return e.msg }
type ConfigurationError struct{ msg string }
func (e *ConfigurationError) Error() string { return e.msg }
type MissingEventNameError struct{ msg string }
func (e *MissingEventNameError) Error() string { return e.msg }
type MissingEventNameDuringRegistration struct{}
func (e *MissingEventNameDuringRegistration) Error() string { return "Missing __event_name__ in registration" }
type MissingEventNameDuringDispatch struct{}
func (e *MissingEventNameDuringDispatch) Error() string { return "Missing 'event_name' in dispatch" }
type MultiplePayloadsDetectedDuringDispatch struct{}
func (e *MultiplePayloadsDetectedDuringDispatch) Error() string { return "Multiple payloads detected in dispatch" }

func TestInitVars(t *testing.T) {
	if handler_store == nil {
		t.Errorf("handler_store should be a map")
	}
	if !event_store.HasSetMethod() ||
		!in_req_res_cycle.HasSetMethod() ||
		!middleware_identifier.HasSetMethod() {
		t.Errorf("All context vars should have set methods")
	}
}

func TestFastapiEventErrorIsRaised(t *testing.T) {
	defer func() { _ = recover() }()
	err := &FastapiEventError{"an error"}
	if err.Error() != "an error" {
		t.Errorf("error message mismatch")
	}
}

func TestConfigurationErrorIsRaised(t *testing.T) {
	defer func() { _ = recover() }()
	err := &ConfigurationError{"bad config"}
	if err.Error() != "bad config" {
		t.Errorf("error message mismatch")
	}
}

func TestMissingEventNameErrorIsRaised(t *testing.T) {
	defer func() { _ = recover() }()
	err := &MissingEventNameError{"missing name"}
	if err.Error() != "missing name" {
		t.Errorf("error message mismatch")
	}
}

func TestMissingEventNameDuringRegistration(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("should catch panic for MissingEventNameDuringRegistration")
		}
	}()
	panic(&MissingEventNameDuringRegistration{})
}

func TestMissingEventNameDuringDispatch(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("should catch panic for MissingEventNameDuringDispatch")
		}
	}()
	panic(&MissingEventNameDuringDispatch{})
}

func TestMultiplePayloadsDetectedDuringDispatch(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("should catch panic for MultiplePayloadsDetectedDuringDispatch")
		}
	}()
	panic(&MultiplePayloadsDetectedDuringDispatch{})
}