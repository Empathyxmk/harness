package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type mockStringReference struct {
	val string
}

func (m *mockStringReference) String() string {
	return m.val
}

type mockTypeReference struct {
	typ string
}

func (m *mockTypeReference) Type() string {
	return m.typ
}

type mockFieldReference struct {
	name string
}

func (m *mockFieldReference) Name() string {
	return m.name
}

type mockMethodReference struct {
	name string
}

func (m *mockMethodReference) Name() string {
	return m.name
}

// Simulated Reference Types and Pool
type ReferenceTypes struct{}

var ReferenceTypesAll = &ReferenceTypes{}

type RefPoolBuffer struct {
	strings []string
	types   []string
	fields  []string
	methods []string
}

func NewRefPoolBuffer(_ *ReferenceTypes) *RefPoolBuffer {
	return &RefPoolBuffer{
		strings: make([]string, 0),
		types:   make([]string, 0),
		fields:  make([]string, 0),
		methods: make([]string, 0),
	}
}

func (b *RefPoolBuffer) Add(val interface{}) {
	switch v := val.(type) {
	case string:
		b.strings = append(b.strings, v)
	case *mockStringReference:
		b.strings = append(b.strings, v.String())
	case *mockTypeReference:
		b.types = append(b.types, v.Type())
	case *mockFieldReference:
		b.fields = append(b.fields, v.Name())
	case *mockMethodReference:
		b.methods = append(b.methods, v.Name())
	}
}

type ReferencePool struct {
	strings []string
	types   []string
	fields  []string
	methods []string
}

func (b *RefPoolBuffer) GetPool(resolve ...bool) *ReferencePool {
	pool := &ReferencePool{
		strings: append([]string{}, b.strings...),
		types:   append([]string{}, b.types...),
		fields:  append([]string{}, b.fields...),
		methods: append([]string{}, b.methods...),
	}
	// Empty buffer after first getPool
	b.strings = []string{}
	b.types = []string{}
	b.fields = []string{}
	b.methods = []string{}
	return pool
}

func (p *ReferencePool) GetStringSection() []string {
	return append([]string{}, p.strings...)
}
func (p *ReferencePool) GetTypeSection() []string {
	return append([]string{}, p.types...)
}
func (p *ReferencePool) GetFieldSection() []string {
	return append([]string{}, p.fields...)
}
func (p *ReferencePool) GetMethodSection() []string {
	return append([]string{}, p.methods...)
}
func (p *ReferencePool) IsEmpty() bool {
	return len(p.strings) == 0 && len(p.types) == 0 && len(p.fields) == 0 && len(p.methods) == 0
}

// ------- Go Test Functions ----------

func TestAddAndGetPool_basic(t *testing.T) {
	buffer := NewRefPoolBuffer(ReferenceTypesAll)
	buffer.Add("string1")
	pool := buffer.GetPool()
	strings := pool.GetStringSection()
	assert.Equal(t, 1, len(strings))
	assert.Equal(t, "string1", strings[0])
	assert.Empty(t, pool.GetTypeSection())
	assert.Empty(t, pool.GetFieldSection())
	assert.Empty(t, pool.GetMethodSection())
}

func TestAddWithReferences(t *testing.T) {
	buffer := NewRefPoolBuffer(ReferenceTypesAll)

	sref := &mockStringReference{val: "S2"}
	buffer.Add(sref)

	tref := &mockTypeReference{typ: "Ltype;"}
	buffer.Add(tref)

	fref := &mockFieldReference{name: "someField"}
	buffer.Add(fref)

	mref := &mockMethodReference{name: "someMethod"}
	buffer.Add(mref)

	pool := buffer.GetPool()
	assert.Equal(t, 1, len(pool.GetStringSection()))
	assert.Equal(t, "S2", pool.GetStringSection()[0])
	assert.Equal(t, 1, len(pool.GetTypeSection()))
	assert.Equal(t, "Ltype;", pool.GetTypeSection()[0])
	assert.Equal(t, 1, len(pool.GetFieldSection()))
	assert.Equal(t, "someField", pool.GetFieldSection()[0])
	assert.Equal(t, 1, len(pool.GetMethodSection()))
	assert.Equal(t, "someMethod", pool.GetMethodSection()[0])
}

func TestGetPoolResolve(t *testing.T) {
	buffer := NewRefPoolBuffer(ReferenceTypesAll)
	buffer.Add("abc")
	pool := buffer.GetPool(true)
	assert.Equal(t, 1, len(pool.GetStringSection()))
	assert.Equal(t, "abc", pool.GetStringSection()[0])
}

func TestGetPoolMultipleCallsReturnsEmptyAfterFirst(t *testing.T) {
	buffer := NewRefPoolBuffer(ReferenceTypesAll)
	buffer.Add("test")
	_ = buffer.GetPool()
	pool2 := buffer.GetPool()
	assert.True(t, pool2.IsEmpty())
}