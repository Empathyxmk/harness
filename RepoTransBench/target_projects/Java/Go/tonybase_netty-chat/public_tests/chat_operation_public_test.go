package public_tests

import (
	"reflect"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

// Simulates: wiki.tony.chat.comet.operation.Operation interface
type Operation interface {
	Op() int
}

type OperationMock struct {
	mock.Mock
}

func (m *OperationMock) Op() int {
	args := m.Called()
	return args.Int(0)
}

// Simulates: ApplicationContext mock (getBeansOfType returns map[string]Operation)
type ApplicationContextMock struct {
	beans map[string]Operation
}

func (c *ApplicationContextMock) GetBeansOfType() map[string]Operation {
	return c.beans
}

// ChatOperation struct and logic
type ChatOperation struct {
	ApplicationContext *ApplicationContextMock
	ops                map[int]Operation
}

// Fill/refresh the internal operation map
func (c *ChatOperation) Operations() map[int]Operation {
	beans := c.ApplicationContext.GetBeansOfType()
	ops := make(map[int]Operation)
	for _, op := range beans {
		if op == nil {
			continue // filter out nil ops
		}
		ops[op.Op()] = op
	}
	c.ops = ops
	return ops
}

// Find operation by op code
func (c *ChatOperation) Find(opcode int) Operation {
	if c.ops == nil {
		c.Operations()
	}
	return c.ops[opcode]
}

func TestChatOperationPublic_OperationsEmpty(t *testing.T) {
	chat := &ChatOperation{ApplicationContext: &ApplicationContextMock{beans: map[string]Operation{"noItem": nil}}}
	ops := chat.Operations()
	assert.NotNil(t, ops)
	// Should filter out nil and ops should be either empty or only have nil values
	if len(ops) == 0 {
		assert.True(t, true)
	} else {
		for _, op := range ops {
			assert.Nil(t, op)
		}
	}
}

func TestChatOperationPublic_OperationsWithOneOperationDifferentOpNumber(t *testing.T) {
	opMock := new(OperationMock)
	opMock.On("Op").Return(22)
	beans := map[string]Operation{"otherOp": opMock}
	chat := &ChatOperation{ApplicationContext: &ApplicationContextMock{beans: beans}}
	ops := chat.Operations()
	assert.NotNil(t, ops)
	assert.Equal(t, 1, len(ops))
	assert.True(t, reflect.DeepEqual(opMock, ops[22]))
}

func TestChatOperationPublic_Find(t *testing.T) {
	opMock := new(OperationMock)
	opMock.On("Op").Return(42)
	beans := map[string]Operation{"deepOp": opMock}
	chat := &ChatOperation{ApplicationContext: &ApplicationContextMock{beans: beans}}
	chat.Operations()
	assert.Equal(t, opMock, chat.Find(42))
	assert.Nil(t, chat.Find(-1))
}