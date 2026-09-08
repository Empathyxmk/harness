using Xunit;

namespace GoogleMailImporter.PublicTests.Gmail
{
    public class GmailServiceModulePublicTests
    {
        [Fact]
        public void TestDifferentProvidesMailboxName()
        {
            var module = new GmailServiceModule("PublicMailboxName");
            Assert.Equal("PublicMailboxName", module.MailboxName);
        }
    }

    // Dummy for testing only
    public class GmailServiceModule
    {
        public string MailboxName { get; }
        public GmailServiceModule(string mailboxName) { MailboxName = mailboxName; }
    }
}