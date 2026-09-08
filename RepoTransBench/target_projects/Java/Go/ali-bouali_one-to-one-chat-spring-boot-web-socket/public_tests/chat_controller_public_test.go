package public_tests

import (
	"net/http"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

// Domain types

type ChatMessage struct {
	Id          string
	SenderId    string
	RecipientId string
	Content     string
}

type ChatNotification struct {
}

type SimpMessagingTemplateMock struct {
	mock.Mock
}

func (m *SimpMessagingTemplateMock) ConvertAndSendToUser(username, dest string, notification interface{}) {
	m.Called(username, dest, notification)
}

type ChatMessageServiceMock struct {
	mock.Mock
}

func (m *ChatMessageServiceMock) Save(msg *ChatMessage) *ChatMessage {
	args := m.Called(msg)
	return args.Get(0).(*ChatMessage)
}
func (m *ChatMessageServiceMock) FindChatMessages(senderId, recipientId string) []*ChatMessage {
	args := m.Called(senderId, recipientId)
	return args.Get(0).([]*ChatMessage)
}

// Subject under test

type ChatController struct {
	MessagingTemplate *SimpMessagingTemplateMock
	MessageService    *ChatMessageServiceMock
}

func (ctrl *ChatController) ProcessMessage(msg *ChatMessage) {
	savedMsg := ctrl.MessageService.Save(msg)
	notification := &ChatNotification{}
	ctrl.MessagingTemplate.ConvertAndSendToUser(msg.RecipientId, "/queue/messages", notification)
	_ = savedMsg
}
func (ctrl *ChatController) FindChatMessages(senderId, recipientId string) (int, []*ChatMessage) {
	messages := ctrl.MessageService.FindChatMessages(senderId, recipientId)
	return http.StatusOK, messages
}

func TestProcessMessageSendsAndSavesMessagePublic(t *testing.T) {
	messaging := new(SimpMessagingTemplateMock)
	msgService := new(ChatMessageServiceMock)
	ctrl := &ChatController{
		MessagingTemplate: messaging,
		MessageService:    msgService,
	}

	msg := &ChatMessage{
		SenderId:    "alice",
		RecipientId: "bob",
		Content:     "Hi Bob!",
		Id:          "msg42",
	}
	msgService.On("Save", msg).Return(msg)
	messaging.On("ConvertAndSendToUser", "bob", "/queue/messages", mock.AnythingOfType("*public_tests.ChatNotification")).Return()

	ctrl.ProcessMessage(msg)

	msgService.AssertCalled(t, "Save", msg)
	messaging.AssertCalled(t, "ConvertAndSendToUser", "bob", "/queue/messages", mock.AnythingOfType("*public_tests.ChatNotification"))
}

func TestFindChatMessagesReturnsMessagesPublic(t *testing.T) {
	messaging := new(SimpMessagingTemplateMock)
	msgService := new(ChatMessageServiceMock)
	ctrl := &ChatController{
		MessagingTemplate: messaging,
		MessageService:    msgService,
	}

	senderId := "charlie"
	recipientId := "dan"
	mockMessages := []*ChatMessage{
		{SenderId: senderId, RecipientId: recipientId, Content: "Good morning"},
		{SenderId: recipientId, RecipientId: senderId, Content: "Hey Charlie!"},
	}
	msgService.On("FindChatMessages", senderId, recipientId).Return(mockMessages)

	status, messages := ctrl.FindChatMessages(senderId, recipientId)

	assert.Equal(t, http.StatusOK, status)
	assert.Len(t, messages, 2)
	assert.Equal(t, mockMessages, messages)
	msgService.AssertCalled(t, "FindChatMessages", senderId, recipientId)
}