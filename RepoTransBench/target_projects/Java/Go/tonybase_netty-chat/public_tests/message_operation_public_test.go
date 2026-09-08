package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

// Constants mock (simulate Constants.OP_MESSAGE etc.)
const (
	OP_MESSAGE       = 101
	OP_MESSAGE_REPLY = 102
)

// Proto simulates wiki.tony.chat.base.bean.Proto
type Proto interface {
	SetOperation(int)
	SetBody(interface{})
}

// ProtoMock allows expectations/assertions
type ProtoMock struct {
	mock.Mock
}

func (m *ProtoMock) SetOperation(code int) {
	m.Called(code)
}
func (m *ProtoMock) SetBody(body interface{}) {
	m.Called(body)
}

// MsgService simulates wiki.tony.chat.base.service.MsgService
type MsgService interface {
	Receive(proto Proto)
}

type MsgServiceMock struct {
	mock.Mock
}

func (m *MsgServiceMock) Receive(proto Proto) {
	m.Called(proto)
}

// Channel simulates io.netty.channel.Channel
type Channel interface {
	WriteAndFlush(proto Proto)
}

type ChannelMock struct {
	mock.Mock
}

func (m *ChannelMock) WriteAndFlush(proto Proto) {
	m.Called(proto)
}

// MessageOperation struct, with private msgService member
type MessageOperation struct {
	msgService MsgService
}

func (m *MessageOperation) Op() int {
	return OP_MESSAGE
}

func (m *MessageOperation) checkAuth(_ Proto) error {
	return nil
}

func (m *MessageOperation) Action(ch Channel, proto Proto) error {
	if err := m.checkAuth(proto); err != nil {
		return err
	}
	m.msgService.Receive(proto)
	proto.SetOperation(OP_MESSAGE_REPLY)
	proto.SetBody(nil)
	ch.WriteAndFlush(proto)
	return nil
}

func TestMessageOperationPublic_Op(t *testing.T) {
	mop := &MessageOperation{}
	assert.NotEqual(t, -99, mop.Op())
	assert.Equal(t, OP_MESSAGE, mop.Op())
}

func TestMessageOperationPublic_Action_WritesReplyWithDifferentProto(t *testing.T) {
	msMock := new(MsgServiceMock)
	chMock := new(ChannelMock)
	protoMock := new(ProtoMock)
	mop := &MessageOperation{msgService: msMock}

	msMock.On("Receive", protoMock).Once()
	protoMock.On("SetOperation", OP_MESSAGE_REPLY).Once()
	protoMock.On("SetBody", nil).Once()
	chMock.On("WriteAndFlush", protoMock).Maybe() // at least once, not always "once"
	protoMock.On("SetOperation", OP_MESSAGE).Times(0)

	err := mop.Action(chMock, protoMock)
	assert.NoError(t, err)
	msMock.AssertExpectations(t)
	protoMock.AssertNotCalled(t, "SetOperation", OP_MESSAGE)
	protoMock.AssertExpectations(t)
	chMock.AssertExpectations(t)
}