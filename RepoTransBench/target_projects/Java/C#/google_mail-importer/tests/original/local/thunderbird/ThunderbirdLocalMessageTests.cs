using Xunit;

namespace GoogleMailImporter.Tests.Original.Local.Thunderbird
{
    public class ThunderbirdLocalMessageTests
    {
        [Fact]
        public void MessageIdDefaultFolder()
        {
            var msg = new ThunderbirdLocalMessage("abc123", "inbox");
            Assert.Equal("abc123", msg.GetMessageId());
            Assert.Contains("inbox", msg.GetFolders());
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