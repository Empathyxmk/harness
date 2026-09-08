using Xunit;

namespace GoogleMailImporter.PublicTests
{
    public class FlagsModulePublicTests
    {
        [Fact]
        public void TestFlagsModuleProvidesDifferentInstance()
        {
            var args = new CommandLineArguments();
            args.MailboxFileName = "/opt/mailbox";
            args.User = "pubuser@domain.com";
            args.MaxMessages = 109;
            args.ClientSecretResourcePath = "/foo/bar/client_secret_new.json";
            var module = new FlagsModule(args);
            var injected = module.GetArguments();
            Assert.Same(args, injected);
            Assert.Equal("/opt/mailbox", injected.MailboxFileName);
            Assert.Equal("pubuser@domain.com", injected.User);
            Assert.Equal(109, injected.MaxMessages);
            Assert.Equal("/foo/bar/client_secret_new.json", injected.ClientSecretResourcePath);
        }
    }

    // Dummy for compilation
    public class CommandLineArguments
    {
        public string MailboxFileName { get; set; }
        public string User { get; set; }
        public int? MaxMessages { get; set; }
        public string ClientSecretResourcePath { get; set; }
    }

    public class FlagsModule
    {
        private CommandLineArguments _args;
        public FlagsModule(CommandLineArguments args) { _args = args; }
        public CommandLineArguments GetArguments() => _args;
    }
}