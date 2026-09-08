package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type SupportV4Fragment struct{}
type Fragment struct{}

type InjectorA struct{}
type InjectorB struct{}

type InjectingFragmentModule struct {
	fragment interface{}
	injector interface{}
}

func NewInjectingFragmentModule(fragment interface{}, injector interface{}) *InjectingFragmentModule {
	return &InjectingFragmentModule{fragment, injector}
}

func (m *InjectingFragmentModule) ProvideSupportV4Fragment() *SupportV4Fragment {
	if f, ok := m.fragment.(*SupportV4Fragment); ok {
		return f
	}
	return nil
}

func (m *InjectingFragmentModule) ProvideFragment() *Fragment {
	if f, ok := m.fragment.(*Fragment); ok {
		return f
	}
	return nil
}

func (m *InjectingFragmentModule) ProvideFragmentInjector() interface{} {
	return m.injector
}

func TestSupportV4FragmentConstructorAndProviderPublic(t *testing.T) {
	v4fragA := &SupportV4Fragment{}
	v4fragB := &SupportV4Fragment{}
	injA := &InjectorA{}
	injB := &InjectorB{}
	modA := NewInjectingFragmentModule(v4fragA, injA)
	modB := NewInjectingFragmentModule(v4fragB, injB)

	provided := modA.ProvideSupportV4Fragment()
	assert.NotNil(t, provided)
	assert.Equal(t, v4fragA, provided)
}

func TestAppFragmentConstructorAndProviderPublic(t *testing.T) {
	fragB := &Fragment{}
	injB := &InjectorB{}
	modB := NewInjectingFragmentModule(fragB, injB)
	provided := modB.ProvideFragment()
	assert.NotNil(t, provided)
	assert.Equal(t, fragB, provided)
}

func TestProvideFragmentInjectorForSupportV4Public(t *testing.T) {
	v4fragA := &SupportV4Fragment{}
	injA := &InjectorA{}
	modA := NewInjectingFragmentModule(v4fragA, injA)
	provided := modA.ProvideFragmentInjector()
	assert.NotNil(t, provided)
	assert.Equal(t, injA, provided)
}

func TestProvideFragmentInjectorForAppFragmentPublic(t *testing.T) {
	fragB := &Fragment{}
	injB := &InjectorB{}
	modB := NewInjectingFragmentModule(fragB, injB)
	provided := modB.ProvideFragmentInjector()
	assert.NotNil(t, provided)
	assert.Equal(t, injB, provided)
}