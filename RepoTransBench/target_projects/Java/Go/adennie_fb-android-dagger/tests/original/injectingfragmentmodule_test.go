package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type SupportV4Fragment struct{}
type Fragment struct{}

type InjectingFragmentModule struct {
	fragment     interface{}
	injector     Injector
}

func NewInjectingFragmentModule(fragment interface{}, injector Injector) *InjectingFragmentModule {
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

func (m *InjectingFragmentModule) ProvideFragmentInjector() Injector {
	return m.injector
}

type DummyInjector struct{}

func TestSupportV4FragmentConstructorAndProvider(t *testing.T) {
	v4frag := &SupportV4Fragment{}
	inj := &DummyInjector{}
	mod := NewInjectingFragmentModule(v4frag, inj)
	provided := mod.ProvideSupportV4Fragment()
	assert.NotNil(t, provided)
	assert.Equal(t, v4frag, provided)
}

func TestAppFragmentConstructorAndProvider(t *testing.T) {
	frag := &Fragment{}
	inj := &DummyInjector{}
	mod := NewInjectingFragmentModule(frag, inj)
	provided := mod.ProvideFragment()
	assert.NotNil(t, provided)
	assert.Equal(t, frag, provided)
}

func TestProvideFragmentInjectorForSupportV4(t *testing.T) {
	v4frag := &SupportV4Fragment{}
	inj := &DummyInjector{}
	mod := NewInjectingFragmentModule(v4frag, inj)
	provided := mod.ProvideFragmentInjector()
	assert.NotNil(t, provided)
	assert.Equal(t, inj, provided)
}

func TestProvideFragmentInjectorForAppFragment(t *testing.T) {
	frag := &Fragment{}
	inj := &DummyInjector{}
	mod := NewInjectingFragmentModule(frag, inj)
	provided := mod.ProvideFragmentInjector()
	assert.NotNil(t, provided)
	assert.Equal(t, inj, provided)
}