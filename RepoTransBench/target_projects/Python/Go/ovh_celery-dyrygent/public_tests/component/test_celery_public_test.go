package component

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type Signature struct {
	name   string
	args   []int
	kwargs map[string]int
}

func NewSignature(name string, args []int, kwargs map[string]int) *Signature {
	return &Signature{name: name, args: args, kwargs: kwargs}
}

type Chord struct {
	header []*Signature
	body   *Signature
}

func NewChord(header []*Signature, body *Signature) *Chord {
	return &Chord{header: header, body: body}
}

type Chain struct {
	tasks []*Signature
}

func NewChain(tasks []*Signature) *Chain {
	return &Chain{tasks: tasks}
}

type Group struct {
	tasks []*Signature
}

func NewGroup(tasks []*Signature) *Group {
	return &Group{tasks: tasks}
}

func TestSignaturePublic(t *testing.T) {
	sig := NewSignature("test_func", []int{9, 8}, map[string]int{"k": 7})
	assert.Equal(t, "test_func", sig.name)
	assert.Equal(t, []int{9, 8}, sig.args)
	assert.Equal(t, 7, sig.kwargs["k"])
}

func TestChordPublic(t *testing.T) {
	header := []*Signature{NewSignature("sigA", []int{1}, nil)}
	body := NewSignature("bodyA", []int{}, nil)
	chord := NewChord(header, body)
	assert.Equal(t, "sigA", chord.header[0].name)
	assert.Equal(t, "bodyA", chord.body.name)
}

func TestChainAndGroupPublic(t *testing.T) {
	c := NewChain([]*Signature{NewSignature("z", nil, nil)})
	g := NewGroup([]*Signature{NewSignature("a", nil, nil), NewSignature("b", []int{1}, nil)})
	assert.Len(t, c.tasks, 1)
	assert.Len(t, g.tasks, 2)
}