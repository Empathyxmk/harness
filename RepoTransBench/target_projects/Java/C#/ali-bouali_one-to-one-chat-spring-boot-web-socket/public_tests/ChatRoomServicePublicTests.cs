using System.Collections.Generic;
using Xunit;

namespace ChatApp.PublicTests
{
    public class ChatRoomServicePublicTests
    {
        // Simulated ChatRoomService implementation to match Java public test logic
        public class ChatRoomService
        {
            private readonly Dictionary<string, string> chatRooms = new Dictionary<string, string>();

            public string? FindChatId(string senderId, string recipientId, bool createIfNotExist)
            {
                var key1 = $"{senderId}:{recipientId}";
                var key2 = $"{recipientId}:{senderId}";

                if (chatRooms.ContainsKey(key1))
                    return chatRooms[key1];
                if (chatRooms.ContainsKey(key2))
                    return chatRooms[key2];

                if (createIfNotExist)
                {
                    var chatId = $"{senderId}_{recipientId}";
                    chatRooms[key1] = chatId;
                    return chatId;
                }
                return null;
            }

            public int TotalChatRooms => chatRooms.Count;
        }

        [Fact]
        public void ShouldCreateChatRoomIfNotExists()
        {
            var service = new ChatRoomService();
            var chatId = service.FindChatId("Tom", "Jerry", true);

            Assert.NotNull(chatId);
            Assert.Equal("Tom_Jerry", chatId);
            Assert.Equal(1, service.TotalChatRooms);
        }

        [Fact]
        public void ShouldReturnSameChatRoomForParticipants()
        {
            var service = new ChatRoomService();
            var id1 = service.FindChatId("userA", "userB", true);

            Assert.NotNull(id1);

            // Should retrieve the same chatId from the other direction
            var id2 = service.FindChatId("userB", "userA", false);

            Assert.NotNull(id2);
            Assert.Equal(id1, id2);

            Assert.Equal(1, service.TotalChatRooms);
        }

        [Fact]
        public void ShouldReturnNullIfRoomDoesNotExistAndNotCreating()
        {
            var service = new ChatRoomService();
            var id = service.FindChatId("not", "exist", false);
            Assert.Null(id);
            Assert.Equal(0, service.TotalChatRooms);
        }

        [Fact]
        public void ShouldNotDuplicateRoom()
        {
            var service = new ChatRoomService();
            var a = service.FindChatId("x", "y", true);
            var b = service.FindChatId("y", "x", true);
            Assert.NotNull(a);
            Assert.Equal(a, b);

            Assert.Equal(1, service.TotalChatRooms);
        }

        [Fact]
        public void ShouldBeCaseSensitive()
        {
            var service = new ChatRoomService();
            var id1 = service.FindChatId("User", "user", true);

            Assert.NotNull(id1);

            var id2 = service.FindChatId("user", "User", false);

            Assert.Null(id2);
            Assert.Equal(1, service.TotalChatRooms);
        }
    }
}