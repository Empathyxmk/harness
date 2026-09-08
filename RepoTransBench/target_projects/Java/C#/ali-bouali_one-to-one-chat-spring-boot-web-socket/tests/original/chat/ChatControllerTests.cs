using System.Collections.Generic;
using Xunit;
using Moq;

namespace ChatApp.Tests.Original.Chat
{
    public class ChatControllerTests
    {
        private Mock<ISimpMessagingTemplate> _messagingTemplateMock;
        private Mock<IChatMessageService> _chatMessageServiceMock;
        private ChatController _chatController;

        public ChatControllerTests()
        {
            _messagingTemplateMock = new Mock<ISimpMessagingTemplate>();
            _chatMessageServiceMock = new Mock<IChatMessageService>();
            _chatController = new ChatController(_chatMessageServiceMock.Object, _messagingTemplateMock.Object);
        }

        [Fact]
        public void ProcessMessage_SendsAndSavesMessage()
        {
            var chatMessage = new ChatMessage
            {
                SenderId = "user1",
                RecipientId = "user2",
                Content = "Hello",
                Id = "msg1"
            };
            _chatMessageServiceMock.Setup(s => s.Save(It.IsAny<ChatMessage>()))
                .Returns(chatMessage);

            _chatController.ProcessMessage(chatMessage);

            _chatMessageServiceMock.Verify(s => s.Save(chatMessage), Times.Once);
            _messagingTemplateMock.Verify(mt =>
                mt.ConvertAndSendToUser(
                    "user2",
                    "/queue/messages",
                    It.IsAny<ChatNotification>()),
                Times.Once
            );
        }

        [Fact]
        public void FindChatMessages_ReturnsMessages()
        {
            string senderId = "user1";
            string recipientId = "user2";
            var mockMessages = new List<ChatMessage>
            {
                new ChatMessage { SenderId = senderId, RecipientId = recipientId, Content = "Hi" },
                new ChatMessage { SenderId = recipientId, RecipientId = senderId, Content = "Hello" }
            };

            _chatMessageServiceMock.Setup(s => s.FindChatMessages(senderId, recipientId)).Returns(mockMessages);

            var response = _chatController.FindChatMessages(senderId, recipientId);

            Assert.Equal(200, response.StatusCode);
            Assert.NotNull(response.Body);
            Assert.Equal(2, response.Body.Count);
            Assert.Equal(mockMessages, response.Body);
            _chatMessageServiceMock.Verify(s => s.FindChatMessages(senderId, recipientId), Times.Once);
        }
    }

    // Mocks/Translations of controller, message, etc.
    public interface ISimpMessagingTemplate
    {
        void ConvertAndSendToUser(string user, string dest, ChatNotification notification);
    }

    public interface IChatMessageService
    {
        ChatMessage Save(ChatMessage msg);
        List<ChatMessage> FindChatMessages(string senderId, string recipientId);
    }

    public class ChatController
    {
        private readonly IChatMessageService _chatMessageService;
        private readonly ISimpMessagingTemplate _messagingTemplate;
        public ChatController(IChatMessageService chatMessageService, ISimpMessagingTemplate messagingTemplate)
        {
            _chatMessageService = chatMessageService;
            _messagingTemplate = messagingTemplate;
        }

        public void ProcessMessage(ChatMessage chatMessage)
        {
            var saved = _chatMessageService.Save(chatMessage);
            _messagingTemplate.ConvertAndSendToUser(
                saved.RecipientId,
                "/queue/messages",
                new ChatNotification() // Details omitted
            );
        }

        public Response<List<ChatMessage>> FindChatMessages(string senderId, string recipientId)
        {
            var msgs = _chatMessageService.FindChatMessages(senderId, recipientId);
            return new Response<List<ChatMessage>>(200, msgs);
        }
    }

    public class ChatMessage
    {
        public string Id { get; set; }
        public string SenderId { get; set; }
        public string RecipientId { get; set; }
        public string Content { get; set; }
    }

    public class ChatNotification { }

    public class Response<T>
    {
        public int StatusCode { get; }
        public T Body { get; }
        public Response(int code, T body)
        {
            StatusCode = code;
            Body = body;
        }
    }
}