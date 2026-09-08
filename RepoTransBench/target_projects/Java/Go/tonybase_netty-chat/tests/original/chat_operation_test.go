package original

import (
	"reflect"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

// --- Mocks and Stubs ---

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
			continue
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

func TestChatOperation_OperationsEmpty(t *testing.T) {
	chat := &ChatOperation{ApplicationContext: &ApplicationContextMock{beans: map[string]Operation{}}}
	ops := chat.Operations()
	assert.NotNil(t, ops)
	assert.True(t, len(ops) == 0, "operations map should be empty")
}

func TestChatOperation_OperationsWithOneOperation(t *testing.T) {
	opMock := new(OperationMock)
	opMock.On("Op").Return(1)
	beans := map[string]Operation{"myOp": opMock}
	chat := &ChatOperation{ApplicationContext: &ApplicationContextMock{beans: beans}}
	ops := chat.Operations()
	assert.NotNil(t, ops)
	assert.Equal(t, 1, len(ops), "should have one operation")
	assert.True(t, reflect.DeepEqual(opMock, ops[1]))
}

func TestChatOperation_Find(t *testing.T) {
	opMock := new(OperationMock)
	opMock.On("Op").Return(5)
	beans := map[string]Operation{"myOp": opMock}
	chat := &ChatOperation{ApplicationContext: &ApplicationContextMock{beans: beans}}
	chat.Operations()
	assert.Equal(t, opMock, chat.Find(5), "should find operation 5")
	assert.Nil(t, chat.Find(99), "should not find nonexistent operation")
}