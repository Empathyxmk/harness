using Xunit;

namespace GoogleMailImporter.Tests.Original
{
    public class FlagsModuleTests
    {
        [Fact]
        public void TestFlagsModuleBindsArguments()
        {
            var args = new CommandLineArguments();
            args.MailboxFileName = "foo";
            var module = new FlagsModule(args);
            var injected = module.GetArguments();
            Assert.Equal("foo", injected.MailboxFileName);
            Assert.Same(args, injected);
        }
    }

    // Dummy placeholder for compilation
    public class FlagsModule
    {
        private CommandLineArguments _args;
        public FlagsModule(CommandLineArguments args) { _args = args; }
        public CommandLineArguments GetArguments() => _args;
    }

    public class CommandLineArguments
    {
        public string MailboxFileName { get; set; }
    }
}