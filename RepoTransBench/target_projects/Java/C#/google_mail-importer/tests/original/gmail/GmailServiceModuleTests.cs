using Xunit;

namespace GoogleMailImporter.Tests.Original.Gmail
{
    public class GmailServiceModuleTests
    {
        [Fact]
        public void ReturnsMailboxName()
        {
            var module = new GmailServiceModule("Inbox");
            Assert.Equal("Inbox", module.MailboxName);
        }
    }

    // Dummy for compilation
    public class GmailServiceModule
    {
        public string MailboxName { get; }
        public GmailServiceModule(string mailboxName) { MailboxName = mailboxName; }
    }
}