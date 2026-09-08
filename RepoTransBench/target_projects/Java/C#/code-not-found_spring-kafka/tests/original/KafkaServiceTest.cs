using System;
using Xunit;
using KafkaServiceApp;

namespace KafkaServiceOriginalTests
{
    public class KafkaServiceTest
    {
        [Fact]
        public void TestProcessMessage_valid()
        {
            var service = new KafkaService();
            var result = service.ProcessMessage("hello world");
            Assert.NotNull(result);
            Assert.Equal("Processed: HELLO WORLD", result);
        }

        [Fact]
        public void TestProcessMessage_null()
        {
            var service = new KafkaService();
            var result = service.ProcessMessage(null);
            Assert.NotNull(result);
            Assert.Equal("Error: Message cannot be empty.", result);
        }

        [Fact]
        public void TestProcessMessage_empty()
        {
            var service = new KafkaService();
            var result = service.ProcessMessage("");
            Assert.NotNull(result);
            Assert.Equal("Error: Message cannot be empty.", result);
        }

        [Fact]
        public void TestProcessMessage_whitespace()
        {
            var service = new KafkaService();
            var result = service.ProcessMessage("   ");
            Assert.NotNull(result);
            Assert.Equal("Error: Message cannot be empty.", result);
        }

        [Fact]
        public void TestProcessMessage_tooLong()
        {
            var service = new KafkaService();
            var longMessage = "This is a very long message that definitely exceeds fifty characters in length and will trigger the warning message condition.";
            var result = service.ProcessMessage(longMessage);
            Assert.NotNull(result);
            Assert.Equal("Warning: Message too long.", result);
        }

        [Fact]
        public void TestProcessMessage_boundaryLengthFifty()
        {
            var service = new KafkaService();
            var fiftyCharMessage = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWX"; // 50 chars
            var result = service.ProcessMessage(fiftyCharMessage);
            Assert.NotNull(result);
            Assert.Equal("Processed: ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWX", result);
        }

        [Fact]
        public void TestProcessMessage_boundaryLengthFiftyOne()
        {
            var service = new KafkaService();
            var fiftyOneCharMessage = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXY"; // 51 chars
            var result = service.ProcessMessage(fiftyOneCharMessage);
            Assert.NotNull(result);
            Assert.Equal("Warning: Message too long.", result);
        }

        [Fact]
        public void TestGetMessageLength_valid()
        {
            var service = new KafkaService();
            var length = service.GetMessageLength("test");
            Assert.Equal(4, length);
        }

        [Fact]
        public void TestGetMessageLength_null()
        {
            var service = new KafkaService();
            var length = service.GetMessageLength(null);
            Assert.Equal(0, length);
        }

        [Fact]
        public void TestGetMessageLength_empty()
        {
            var service = new KafkaService();
            var length = service.GetMessageLength("");
            Assert.Equal(0, length);
        }
    }
}