package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// Simulate ReferencePool logic from Java for testing.
type ReferencePool2 struct {
	strings []string
	types   []string
	fields  []string
	methods []string
}

func newReferencePool2() *ReferencePool2 {
	return &ReferencePool2{
		strings: []string{},
		types:   []string{},
		fields:  []string{},
		methods: []string{},
	}
}

func (pool *ReferencePool2) AddString(s string) {
	pool.strings = append(pool.strings, s)
}
func (pool *ReferencePool2) AddType(t string) {
	pool.types = append(pool.types, t)
}
func (pool *ReferencePool2) AddField(f string) {
	pool.fields = append(pool.fields, f)
}
func (pool *ReferencePool2) AddMethod(m string) {
	pool.methods = append(pool.methods, m)
}
func (pool *ReferencePool2) CountStrings() int {
	return len(pool.strings)
}
func (pool *ReferencePool2) CountTypes() int {
	return len(pool.types)
}
func (pool *ReferencePool2) CountFields() int {
	return len(pool.fields)
}
func (pool *ReferencePool2) CountMethods() int {
	return len(pool.methods)
}
func (pool *ReferencePool2) IsEmpty() bool {
	return len(pool.strings) == 0 && len(pool.types) == 0 && len(pool.fields) == 0 && len(pool.methods) == 0
}

func TestReferencePool_AddStringAndCount(t *testing.T) {
	pool := newReferencePool2()
	assert.True(t, pool.IsEmpty())
	pool.AddString("one")
	pool.AddString("two")
	count := pool.CountStrings()
	assert.Equal(t, 2, count)
	assert.False(t, pool.IsEmpty())
}

func TestReferencePool_AddTypeAndCount(t *testing.T) {
	pool := newReferencePool2()
	pool.AddType("Lfoo;")
	pool.AddType("Lbar;")
	count := pool.CountTypes()
	assert.Equal(t, 2, count)
}

func TestReferencePool_AddFieldAndMethodAndCount(t *testing.T) {
	pool := newReferencePool2()
	pool.AddField("field1")
	pool.AddField("field2")
	assert.Equal(t, 2, pool.CountFields())
	pool.AddMethod("meth1")
	assert.Equal(t, 1, pool.CountMethods())
}

func TestReferencePool_EmptyPoolBehavior(t *testing.T) {
	pool := newReferencePool2()
	assert.True(t, pool.IsEmpty())
}