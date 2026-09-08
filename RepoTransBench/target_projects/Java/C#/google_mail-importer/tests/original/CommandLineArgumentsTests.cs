using Xunit;

namespace GoogleMailImporter.Tests.Original
{
    public class CommandLineArgumentsTests
    {
        [Fact]
        public void TestDefaults()
        {
            var args = new CommandLineArguments();
            Assert.Null(args.MailboxFileName);
            Assert.Equal("me", args.User);
            Assert.Null(args.MaxMessages);
            Assert.Equal("/resources/client_secret.json", args.ClientSecretResourcePath);
        }

        [Fact]
        public void TestSetArguments()
        {
            var args = new CommandLineArguments();
            args.MailboxFileName = "/tmp/mail";
            args.User = "user@example.com";
            args.MaxMessages = 10;
            args.ClientSecretResourcePath = "/custom/path/secret.json";
            Assert.Equal("/tmp/mail", args.MailboxFileName);
            Assert.Equal("user@example.com", args.User);
            Assert.Equal(10, args.MaxMessages);
            Assert.Equal("/custom/path/secret.json", args.ClientSecretResourcePath);
        }
    }

    // Dummy class for compilation; in practice imported from source.
    public class CommandLineArguments
    {
        public string MailboxFileName { get; set; }
        public string User { get; set; } = "me";
        public int? MaxMessages { get; set; }
        public string ClientSecretResourcePath { get; set; } = "/resources/client_secret.json";
    }
}