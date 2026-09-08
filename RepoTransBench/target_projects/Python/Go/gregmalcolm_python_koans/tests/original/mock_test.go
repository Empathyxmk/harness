package original

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

// SentinelObject test
type SentinelObject struct {
	label string
}

func (so *SentinelObject) String() string {
	return "<SentinelObject \"" + so.label + "\">"
}

// Sentinel type: just a struct for attribute uniqueness
type Sentinel struct {
	values map[string]*SentinelObject
}

func NewSentinel() *Sentinel {
	return &Sentinel{values: make(map[string]*SentinelObject)}
}

func (s *Sentinel) Attr(name string) *SentinelObject {
	if v, ok := s.values[name]; ok {
		return v
	}
	obj := &SentinelObject{label: name}
	s.values[name] = obj
	return obj
}

// ClassType is always a type (for test)
type ClassType struct{}

var sentinel = struct {
	DEFAULT string
}{DEFAULT: "default"}

func dotLookup(x interface{}, name string) interface{} {
	switch obj := x.(type) {
	case map[string]interface{}:
		return obj[name]
	case struct{ Foo int }:
		return obj.Foo
	case *X:
		return obj.Foo
	}
	return nil
}

type X struct {
	Foo int
}

func _copy(val interface{}) interface{} {
	switch v := val.(type) {
	case []int:
		c := make([]int, len(v))
		copy(c, v)
		return c
	case map[string]interface{}:
		cp := make(map[string]interface{})
		for k, val := range v {
			cp[k] = val
		}
		return cp
	case [2]int:
		return [2]int{v[0], v[1]}
	case int:
		return v
	}
	return val
}

type Mock struct {
	called      bool
	callCount   int
	callArgs    []interface{}
	returnValue interface{}
	sideEffect  func(args ...interface{}) interface{}
	specFields  map[string]struct{}
}

func NewMock() *Mock {
	return &Mock{specFields: make(map[string]struct{})}
}
func (m *Mock) Call(args ...interface{}) interface{} {
	m.called = true
	m.callCount++
	m.callArgs = args
	if m.sideEffect != nil {
		return m.sideEffect(args...)
	}
	return m.returnValue
}
func (m *Mock) ResetMock() {
	m.called = false
	m.callCount = 0
	m.callArgs = nil
}
func (m *Mock) AssertCalledWith(args ...interface{}) error {
	for i, arg := range args {
		if i < len(m.callArgs) {
			if m.callArgs[i] != arg {
				return errors.New("call args mismatch")
			}
		}
	}
	return nil
}
func (m *Mock) SetReturnValue(v interface{}) {
	m.returnValue = v
}
func (m *Mock) SetSideEffect(f func(args ...interface{}) interface{}) {
	m.sideEffect = f
}
func (m *Mock) SetSpec(fields []string) {
	for _, name := range fields {
		m.specFields[name] = struct{}{}
	}
}
func (m *Mock) Attr(name string) (interface{}, error) {
	if len(m.specFields) > 0 {
		if _, ok := m.specFields[name]; !ok {
			return nil, errors.New("attribute not allowed")
		}
	}
	return nil, nil
}
func (m *Mock) SetWraps(fn func(int) int) {
	m.sideEffect = func(args ...interface{}) interface{} {
		return fn(args[0].(int))
	}
}

func TestSentinelObjectRepr(t *testing.T) {
	s := &SentinelObject{label: "MY_MARK"}
	assert.Equal(t, `<SentinelObject "MY_MARK">`, s.String())
}

func TestSentinelAttributeUniqueness(t *testing.T) {
	s := NewSentinel()
	a := s.Attr("foo")
	b := s.Attr("foo")
	c := s.Attr("bar")
	assert.True(t, a == b)
	assert.True(t, a != c)
}

func TestDefaultAndClassType(t *testing.T) {
	assert.Equal(t, "default", sentinel.DEFAULT)
}

func TestDotLookupBasic(t *testing.T) {
	x := &X{Foo: 123}
	assert.Equal(t, 123, dotLookup(x, "foo"))
}

func TestCopyListsDictsTuplesSets(t *testing.T) {
	lst := []int{1, 2}
	copied := _copy(lst).([]int)
	assert.ElementsMatch(t, lst, copied)
	dct := map[string]interface{}{"a": 1}
	copiedMap := _copy(dct).(map[string]interface{})
	assert.Equal(t, dct, copiedMap)
	tpl := [2]int{1, 2}
	copiedTpl := _copy(tpl).([2]int)
	assert.Equal(t, tpl, copiedTpl)
	s := 12
	assert.Equal(t, s, _copy(s))
}

func TestMockBasicsAndMethods(t *testing.T) {
	m := NewMock()
	m.Call(1, 2, 3)
	assert.True(t, m.called)
	assert.Equal(t, 1, m.callCount)
	m.ResetMock()
	assert.False(t, m.called)
	m2 := NewMock()
	m2.SetReturnValue("abc")
	rv := m2.Call()
	assert.Equal(t, "abc", rv)
	m2.Call(1, 2)
	assert.Nil(t, m2.AssertCalledWith(1, 2))
}

func TestMockSideEffectLambda(t *testing.T) {
	m := NewMock()
	m.SetSideEffect(func(args ...interface{}) interface{} {
		return args[0].(int) * 2
	})
	assert.Equal(t, 8, m.Call(4))
}

func TestMockSideEffectException(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Should have panicked")
		}
	}()
	m := NewMock()
	m.SetSideEffect(func(args ...interface{}) interface{} { panic("fail") })
	m.Call()
}

func TestMockSpecBlocksNonexistent(t *testing.T) {
	m := NewMock()
	m.SetSpec([]string{"foo"})
	_, err := m.Attr("foo")
	assert.NoError(t, err)
	_, err = m.Attr("bar")
	assert.Error(t, err)
}

func TestMockWraps(t *testing.T) {
	fn := func(x int) int { return x + 1 }
	m := NewMock()
	m.SetWraps(fn)
	assert.Equal(t, 4, m.Call(3))
}