package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

type ChatRoom struct {
	ChatId      string
	SenderId    string
	RecipientId string
}

type ChatRoomRepositoryMock struct {
	mock.Mock
}

func (m *ChatRoomRepositoryMock) FindBySenderIdAndRecipientId(senderId, recipientId string) (*ChatRoom, bool) {
	args := m.Called(senderId, recipientId)
	cr := args.Get(0)
	if cr == nil {
		return nil, false
	}
	return cr.(*ChatRoom), true
}

func (m *ChatRoomRepositoryMock) Save(chatRoom *ChatRoom) *ChatRoom {
	args := m.Called(chatRoom)
	return args.Get(0).(*ChatRoom)
}

type ChatRoomService struct {
	Repository *ChatRoomRepositoryMock
}

func (service *ChatRoomService) getChatRoomId(senderId, recipientId string, createIfNotExists bool) (string, bool) {
	if chatRoom, found := service.Repository.FindBySenderIdAndRecipientId(senderId, recipientId); found {
		return chatRoom.ChatId, true
	}
	if !createIfNotExists {
		return "", false
	}
	chatId := senderId + "_" + recipientId
	r := &ChatRoom{ChatId: chatId, SenderId: senderId, RecipientId: recipientId}
	service.Repository.Save(r)
	r2 := &ChatRoom{ChatId: chatId, SenderId: recipientId, RecipientId: senderId}
	service.Repository.Save(r2)
	return chatId, true
}

func TestGetChatRoomIdExistingRoomPublic(t *testing.T) {
	repo := new(ChatRoomRepositoryMock)
	service := &ChatRoomService{Repository: repo}

	senderId := "alice"
	recipientId := "bob"
	expectedChatId := "alice_bob"

	room := &ChatRoom{ChatId: expectedChatId, SenderId: senderId, RecipientId: recipientId}

	repo.On("FindBySenderIdAndRecipientId", senderId, recipientId).Return(room)

	chatId, ok := service.getChatRoomId(senderId, recipientId, false)

	assert.True(t, ok)
	assert.Equal(t, expectedChatId, chatId)
	repo.AssertNotCalled(t, "Save", mock.Anything)
}

func TestGetChatRoomIdNewRoomCreateIfNotExistsTruePublic(t *testing.T) {
	repo := new(ChatRoomRepositoryMock)
	service := &ChatRoomService{Repository: repo}

	senderId := "charlie"
	recipientId := "dan"
	expectedChatId := "charlie_dan"

	repo.On("FindBySenderIdAndRecipientId", senderId, recipientId).Return(nil)
	repo.On("Save", mock.AnythingOfType("*public_tests.ChatRoom")).Return(func(chatRoom *ChatRoom) *ChatRoom { return chatRoom })

	chatId, ok := service.getChatRoomId(senderId, recipientId, true)

	assert.True(t, ok)
	assert.Equal(t, expectedChatId, chatId)
	repo.AssertNumberOfCalls(t, "Save", 2)
}

func TestGetChatRoomIdNewRoomCreateIfNotExistsFalsePublic(t *testing.T) {
	repo := new(ChatRoomRepositoryMock)
	service := &ChatRoomService{Repository: repo}

	senderId := "eve"
	recipientId := "frank"

	repo.On("FindBySenderIdAndRecipientId", senderId, recipientId).Return(nil)

	chatId, ok := service.getChatRoomId(senderId, recipientId, false)

	assert.False(t, ok)
	assert.Equal(t, "", chatId)
	repo.AssertNotCalled(t, "Save", mock.Anything)
}