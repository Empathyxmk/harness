package original

import (
	"sync"
	"sync/atomic"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

// --- Mock & Test Stubs ---

type MockRocketMQTemplate struct {
	mock.Mock
}

func (m *MockRocketMQTemplate) SyncSend(topic string, msg interface{}) interface{} {
	args := m.Called(topic, msg)
	return args.Get(0)
}

func (m *MockRocketMQTemplate) SyncSendMessage(topic string, msg Message) interface{} {
	args := m.Called(topic, msg)
	return args.Get(0)
}

func (m *MockRocketMQTemplate) SendMessageInTransaction(topic string, msg Message, arg interface{}) interface{} {
	args := m.Called(topic, msg, arg)
	return args.Get(0)
}

type Message map[string]interface{}

type ProducerACLApplication struct {
	rocketMQTemplate interface {
		SyncSend(string, interface{}) interface{}
		SyncSendMessage(string, Message) interface{}
		SendMessageInTransaction(string, Message, interface{}) interface{}
	}
	springTransTopic string
	springTopic      string
}

// The TransactionListenerImpl inner class logic from Java
type TransactionListenerImpl struct {
	transactionIndex int32
	localTrans       sync.Map
}

type RocketMQLocalTransactionState int

const (
	Commit RocketMQLocalTransactionState = iota
	Rollback
	Unknown
)

// Java logic simulated: each execute increments an index, and cycles through 0/1/else
func (t *TransactionListenerImpl) ExecuteLocalTransaction(msg Message, arg interface{}) RocketMQLocalTransactionState {
	index := int(atomic.AddInt32(&t.transactionIndex, 1)) % 3
	switch index {
	case 1:
		return Commit
	case 2:
		return Rollback
	default:
		return Unknown
	}
}

func (t *TransactionListenerImpl) CheckLocalTransaction(msg Message) RocketMQLocalTransactionState {
	txID, _ := msg["TRANSACTION_ID"].(string)
	val, ok := t.localTrans.Load(txID)
	if !ok {
		return Unknown
	}
	switch v := val.(int); v {
	case 0:
		return Commit
	case 1:
		return Rollback
	default:
		return Unknown
	}
}

func (p *ProducerACLApplication) run() {
	p.rocketMQTemplate.SyncSend(p.springTopic, "StringMsg")
	msg := Message{}
	p.rocketMQTemplate.SyncSendMessage(p.springTopic, msg)
	p.rocketMQTemplate.SendMessageInTransaction(p.springTransTopic, msg, nil)
}

func (p *ProducerACLApplication) main(args []string) {}

func TestProducerACLApplication_Run(t *testing.T) {
	mockTemplate := new(MockRocketMQTemplate)
	app := &ProducerACLApplication{
		rocketMQTemplate: mockTemplate,
		springTransTopic: "aclTransTopic",
		springTopic:      "aclTopic",
	}
	mockTemplate.On("SyncSend", mock.Anything, mock.Anything).Return(struct{}{}).Maybe()
	mockTemplate.On("SyncSendMessage", mock.Anything, mock.Anything).Return(struct{}{}).Maybe()
	mockTemplate.On("SendMessageInTransaction", mock.Anything, mock.Anything, mock.Anything).Return(struct{}{}).Maybe()

	app.run()

	mockTemplate.AssertCalled(t, "SyncSend", mock.Anything, mock.Anything)
	mockTemplate.AssertCalled(t, "SyncSendMessage", mock.Anything, mock.Anything)
	mockTemplate.AssertCalled(t, "SendMessageInTransaction", mock.Anything, mock.Anything, mock.Anything)
}

func TestProducerACLApplication_TransactionListenerImpl_executeLocalTransaction_commit(t *testing.T) {
	listener := &TransactionListenerImpl{}
	// Simulate 3 cycles: commit, rollback, unknown
	msg := Message{"TRANSACTION_ID": "tx_1"}
	listener.transactionIndex = 0
	assert.Equal(t, Commit, listener.ExecuteLocalTransaction(msg, nil))
	assert.Equal(t, Rollback, listener.ExecuteLocalTransaction(msg, nil))
	assert.Equal(t, Unknown, listener.ExecuteLocalTransaction(msg, nil))
}

func TestProducerACLApplication_TransactionListenerImpl_checkLocalTransaction_allcases(t *testing.T) {
	listener := &TransactionListenerImpl{}
	txId := "txId"
	listener.localTrans = sync.Map{}
	listener.localTrans.Store(txId, 0)
	msg := Message{"TRANSACTION_ID": txId}
	assert.Equal(t, Commit, listener.CheckLocalTransaction(msg))
	listener.localTrans.Store(txId, 1)
	assert.Equal(t, Rollback, listener.CheckLocalTransaction(msg))
	listener.localTrans.Store(txId, 2)
	assert.Equal(t, Unknown, listener.CheckLocalTransaction(msg))
	listener.localTrans.Delete(txId)
	assert.Equal(t, Unknown, listener.CheckLocalTransaction(msg))
}

func TestProducerACLApplication_Main(t *testing.T) {
	app := &ProducerACLApplication{}
	app.main([]string{})
}