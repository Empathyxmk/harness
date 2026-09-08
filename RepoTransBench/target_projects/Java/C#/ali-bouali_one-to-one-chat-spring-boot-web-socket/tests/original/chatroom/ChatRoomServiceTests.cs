using System.Collections.Generic;
using Xunit;

namespace ChatApp.Tests.ChatRoom
{
    public class ChatRoomServiceTests
    {
        // Simulated ChatRoomService implementation to match Java logic
        public class ChatRoomService
        {
            // Key is user1:user2; Value is chatId (string)
            private readonly Dictionary<string, string> chatRooms = new Dictionary<string, string>();

            public string? FindChatId(string senderId, string recipientId, bool createIfNotExist)
            {
                // Sorted key to simulate uniqueness between pairs, as likely in Java tests
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
        public void FindChatId_ReturnsChatId_IfExists()
        {
            var service = new ChatRoomService();
            // Pre-create a chat room
            var id = service.FindChatId("user1", "user2", true);

            // Now searching again should find it (from either direction)
            var result = service.FindChatId("user1", "user2", false);
            Assert.NotNull(result);
            Assert.Equal(id, result);

            var reverseResult = service.FindChatId("user2", "user1", false);
            Assert.NotNull(reverseResult);
            Assert.Equal(id, reverseResult);
            Assert.Equal(1, service.TotalChatRooms);
        }

        [Fact]
        public void FindChatId_DoesNotCreate_WhenFlagIsFalse()
        {
            var service = new ChatRoomService();
            var result = service.FindChatId("user3", "user4", false);
            Assert.Null(result);
            Assert.Equal(0, service.TotalChatRooms);
        }

        [Fact]
        public void FindChatId_CreatesRoom_WhenNotExists_AndFlagIsTrue()
        {
            var service = new ChatRoomService();
            var result = service.FindChatId("uA", "uB", true);
            Assert.NotNull(result);
            Assert.Equal("uA_uB", result);
            Assert.Equal(1, service.TotalChatRooms);
        }

        [Fact]
        public void FindChatId_ReturnsNull_ForDifferentUnrelatedUsers()
        {
            var service = new ChatRoomService();
            // precreate unrelated chat
            var created = service.FindChatId("alice", "bob", true);

            var notFound = service.FindChatId("charlie", "david", false);
            Assert.Null(notFound);

            Assert.Equal(1, service.TotalChatRooms);
        }

        [Fact]
        public void FindChatId_CaseInsensitive_ShouldNotMatch()
        {
            var service = new ChatRoomService();
            var id1 = service.FindChatId("User1", "User2", true);

            var id2 = service.FindChatId("user1", "user2", false);

            // Should not match because keys are case-sensitive in this implementation
            Assert.Null(id2);
            Assert.Equal(1, service.TotalChatRooms);
        }

        [Fact]
        public void FindChatId_MultipleRooms()
        {
            var service = new ChatRoomService();
            var a = service.FindChatId("A", "B", true);
            var b = service.FindChatId("B", "C", true);
            var c = service.FindChatId("C", "D", true);

            Assert.NotNull(a);
            Assert.NotNull(b);
            Assert.NotNull(c);

            Assert.Equal("A_B", a);
            Assert.Equal("B_C", b);
            Assert.Equal("C_D", c);

            Assert.Equal(3, service.TotalChatRooms);
        }

        [Fact]
        public void FindChatId_SameRoom_NotDuplicated()
        {
            var service = new ChatRoomService();
            var id = service.FindChatId("foo", "bar", true);

            var again = service.FindChatId("foo", "bar", true);
            var reverse = service.FindChatId("bar", "foo", true);

            Assert.Equal(id, again);
            Assert.Equal(id, reverse);
            Assert.Equal(1, service.TotalChatRooms);
        }
    }
}