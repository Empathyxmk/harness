package prototype

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// ---- Mock minimal interface and struct for translation correctness -----

// HelloWorld interface for HelloWorldPrototype
type HelloWorld interface {
	HelloWorld() string
}

type HelloWorldPrototype struct {
	Message string
}

func NewHelloWorldPrototype(msg string) *HelloWorldPrototype {
	return &HelloWorldPrototype{Message: msg}
}

// Static constant/field for prototype (simulated as global variable)
var PROTOTYPE = &HelloWorldPrototype{Message: "Hello Prototype!"}

func (h *HelloWorldPrototype) HelloWorld() string {
	return h.Message
}

// Clone returns a shallow copy implementing HelloWorld interface
func (h *HelloWorldPrototype) Clone() HelloWorld {
	return &HelloWorldPrototype{Message: h.Message}
}

// -------------------------------------------------------------------------

func TestHelloWorldPrototype_CloneAndMessage(t *testing.T) {
	proto := NewHelloWorldPrototype("Test Prototype!")
	cloned := proto.Clone()
	_, ok := cloned.(*HelloWorldPrototype)
	assert.True(t, ok, "cloned should be of type *HelloWorldPrototype")
	assert.Equal(t, "Test Prototype!", cloned.HelloWorld())
}

func TestHelloWorldPrototype_Constant(t *testing.T) {
	assert.Equal(t, "Hello Prototype!", PROTOTYPE.HelloWorld())
	copy := PROTOTYPE.Clone()
	_, ok := copy.(*HelloWorldPrototype)
	assert.True(t, ok, "copy should be of type *HelloWorldPrototype")
	assert.Equal(t, "Hello Prototype!", copy.HelloWorld())
}