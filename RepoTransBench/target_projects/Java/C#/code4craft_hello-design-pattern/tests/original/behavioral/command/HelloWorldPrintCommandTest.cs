using Xunit;

namespace HelloDesignPattern.Tests.behavioral.command
{
    public class HelloWorldPrintCommandTest
    {
        [Fact]
        public void TestPrintCommand()
        {
            var cmd = new HelloWorldPrintCommand();
            cmd.Execute();
        }
    }
}