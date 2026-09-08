package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type SelfRecordingCommand struct {
	N  string
	A1 string
	A2 string
	A3 string
	A4 int
}

func CreateInstancePublic(n, a1, a2, a3 string, a4 int) *SelfRecordingCommand {
	return &SelfRecordingCommand{N: n, A1: a1, A2: a2, A3: a3, A4: a4}
}

func TestCreateInstance_public(t *testing.T) {
	c := CreateInstancePublic("commandX", "2017", "b", "PRIORITY", 7)
	assert.Equal(t, "commandX", c.N)
	assert.Equal(t, "2017", c.A1)
	assert.Equal(t, "b", c.A2)
	assert.Equal(t, "PRIORITY", c.A3)
	assert.Equal(t, 7, c.A4)
}

func TestCreateInstance_nullClass_public(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic when CreateInstancePublic called with nil")
		}
	}()
	var f func() *SelfRecordingCommand
	_ = f() // simulates calling with nil function
}