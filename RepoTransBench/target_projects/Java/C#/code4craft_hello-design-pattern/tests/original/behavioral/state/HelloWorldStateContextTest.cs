using Xunit;

namespace HelloDesignPattern.Tests.behavioral.state
{
    public class HelloWorldStateContextTest
    {
        [Fact]
        public void TestHelloWorldStateContext()
        {
            var helloWorldStateContext = new HelloWorldStateContext();
            helloWorldStateContext.AppendWord("Hello");
            Assert.Equal("Hello ", helloWorldStateContext.HelloWorld());
            helloWorldStateContext.AppendWord("State");
            Assert.Equal("Hello State!", helloWorldStateContext.HelloWorld());
            helloWorldStateContext.AppendWord("Whatever");
            Assert.Equal("Hello State!", helloWorldStateContext.HelloWorld());
        }
    }
}