using Xunit;

namespace GoogleMailImporter.PublicTests.Local.Thunderbird
{
    public class ThunderbirdLocalMessagePublicTests
    {
        [Fact]
        public void TestDifferentMessageIdDefaultFolder()
        {
            var msg = new ThunderbirdLocalMessage("xyz789", "public_folder");
            Assert.Equal("xyz789", msg.GetMessageId());
            Assert.Contains("public_folder", msg.GetFolders());
        }
    }

    public class ThunderbirdLocalMessage
    {
        private readonly string _messageId;
        private readonly string _folder;
        public ThunderbirdLocalMessage(string messageId, string folder)
        {
            _messageId = messageId;
            _folder = folder;
        }
        public string GetMessageId() => _messageId;
        public string[] GetFolders() => new[] { _folder };
    }
}