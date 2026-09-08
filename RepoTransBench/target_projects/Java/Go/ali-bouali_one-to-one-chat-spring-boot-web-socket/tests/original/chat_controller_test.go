package original

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
	// Placeholder for whatever fields you'd need
}

// Mocked dependencies

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

func TestProcessMessageSendsAndSavesMessage(t *testing.T) {
	messaging := new(SimpMessagingTemplateMock)
	msgService := new(ChatMessageServiceMock)
	ctrl := &ChatController{
		MessagingTemplate: messaging,
		MessageService:    msgService,
	}
	msg := &ChatMessage{
		SenderId:    "user1",
		RecipientId: "user2",
		Content:     "Hello",
		Id:          "msg1",
	}
	msgService.On("Save", msg).Return(msg)
	messaging.On("ConvertAndSendToUser", "user2", "/queue/messages", mock.AnythingOfType("*original.ChatNotification")).Return()

	ctrl.ProcessMessage(msg)

	msgService.AssertCalled(t, "Save", msg)
	messaging.AssertCalled(t, "ConvertAndSendToUser", "user2", "/queue/messages", mock.AnythingOfType("*original.ChatNotification"))
}

func TestFindChatMessagesReturnsMessages(t *testing.T) {
	messaging := new(SimpMessagingTemplateMock)
	msgService := new(ChatMessageServiceMock)
	ctrl := &ChatController{
		MessagingTemplate: messaging,
		MessageService:    msgService,
	}

	senderId := "user1"
	recipientId := "user2"
	mockMessages := []*ChatMessage{
		{SenderId: senderId, RecipientId: recipientId, Content: "Hi"},
		{SenderId: recipientId, RecipientId: senderId, Content: "Hello"},
	}
	msgService.On("FindChatMessages", senderId, recipientId).Return(mockMessages)

	status, messages := ctrl.FindChatMessages(senderId, recipientId)

	assert.Equal(t, http.StatusOK, status)
	assert.Len(t, messages, 2)
	assert.Equal(t, mockMessages, messages)
	msgService.AssertCalled(t, "FindChatMessages", senderId, recipientId)
}