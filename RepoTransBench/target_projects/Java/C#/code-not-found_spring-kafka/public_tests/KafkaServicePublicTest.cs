using System;
using Xunit;
using KafkaServiceApp;

namespace KafkaServicePublicTests
{
    public class KafkaServicePublicTest
    {
        [Fact]
        public void TestProcessMessage_valid_diff()
        {
            var service = new KafkaService();
            var result = service.ProcessMessage("Kafka Rocks");
            Assert.NotNull(result);
            Assert.Equal("Processed: KAFKA ROCKS", result);
        }

        [Fact]
        public void TestProcessMessage_null_public()
        {
            var service = new KafkaService();
            var result = service.ProcessMessage(null);
            Assert.NotNull(result);
            Assert.Equal("Error: Message cannot be empty.", result);
        }

        [Fact]
        public void TestProcessMessage_empty_public()
        {
            var service = new KafkaService();
            var result = service.ProcessMessage("");
            Assert.NotNull(result);
            Assert.Equal("Error: Message cannot be empty.", result);
        }

        [Fact]
        public void TestProcessMessage_whitespace_public()
        {
            var service = new KafkaService();
            var result = service.ProcessMessage("\t\n");
            Assert.NotNull(result);
            Assert.Equal("Error: Message cannot be empty.", result);
        }

        [Fact]
        public void TestProcessMessage_tooLong_public()
        {
            var service = new KafkaService();
            var longMessage = "Short messages are nice, but this one is way too long!!!";
            var result = service.ProcessMessage(longMessage);
            Assert.NotNull(result);
            Assert.Equal("Warning: Message too long.", result);
        }

        [Fact]
        public void TestProcessMessage_boundaryLengthFifty_public()
        {
            var service = new KafkaService();
            var msg = "12345678901234567890123456789012345678901234567890"; // 50 chars
            var result = service.ProcessMessage(msg);
            Assert.NotNull(result);
            Assert.Equal("Processed: 12345678901234567890123456789012345678901234567890", result);
        }

        [Fact]
        public void TestProcessMessage_boundaryLengthFiftyOne_public()
        {
            var service = new KafkaService();
            var msg = "123456789012345678901234567890123456789012345678901"; // 51 chars
            var result = service.ProcessMessage(msg);
            Assert.NotNull(result);
            Assert.Equal("Warning: Message too long.", result);
        }

        [Fact]
        public void TestGetMessageLength_valid_public()
        {
            var service = new KafkaService();
            var length = service.GetMessageLength("Kafka");
            Assert.Equal(5, length);
        }

        [Fact]
        public void TestGetMessageLength_null_public()
        {
            var service = new KafkaService();
            var length = service.GetMessageLength(null);
            Assert.Equal(0, length);
        }

        [Fact]
        public void TestGetMessageLength_empty_public()
        {
            var service = new KafkaService();
            var length = service.GetMessageLength("   ".Trim());
            Assert.Equal(0, length);
        }
    }
}