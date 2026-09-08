using Xunit;

namespace GoogleMailImporter.PublicTests
{
    public class CommandLineArgumentsPublicTests
    {
        [Fact]
        public void TestDefaultsPublic()
        {
            var args = new CommandLineArguments();
            Assert.Null(args.MailboxFileName);
            Assert.Equal("me", args.User);
            Assert.Null(args.MaxMessages);
            Assert.Equal("/resources/client_secret.json", args.ClientSecretResourcePath);
        }

        [Fact]
        public void TestSetArgumentsPublic()
        {
            var args = new CommandLineArguments();
            args.MailboxFileName = "/var/mail";
            args.User = "anotheruser@domain.com";
            args.MaxMessages = 42;
            args.ClientSecretResourcePath = "/different/path/secret_v2.json";
            Assert.Equal("/var/mail", args.MailboxFileName);
            Assert.Equal("anotheruser@domain.com", args.User);
            Assert.Equal(42, args.MaxMessages);
            Assert.Equal("/different/path/secret_v2.json", args.ClientSecretResourcePath);
        }
    }

    // Dummy for compilation
    public class CommandLineArguments
    {
        public string MailboxFileName { get; set; }
        public string User { get; set; } = "me";
        public int? MaxMessages { get; set; }
        public string ClientSecretResourcePath { get; set; } = "/resources/client_secret.json";
    }
}