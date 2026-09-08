using Xunit;

namespace HelloDesignPattern.Tests.behavioral.strategy
{
    public class HelloWorldStrategyContextTest
    {
        [Fact]
        public void TestHelloWorldStrategyContext()
        {
            var helloWorldStrategyContext = new HelloWorldStrategyContext(new JavaHelloWorldStrategy());
            Assert.Equal("Hello Java!", helloWorldStrategyContext.HelloWorld());
            helloWorldStrategyContext = new HelloWorldStrategyContext(new DesignPatternHelloWorldStrategy());
            Assert.Equal("Hello Strategy!", helloWorldStrategyContext.HelloWorld());
        }
    }
}