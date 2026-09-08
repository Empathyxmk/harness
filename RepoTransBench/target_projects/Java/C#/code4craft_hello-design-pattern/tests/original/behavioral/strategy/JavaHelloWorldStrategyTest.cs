using Xunit;

namespace HelloDesignPattern.Tests.behavioral.strategy
{
    public class JavaHelloWorldStrategyTest
    {
        [Fact]
        public void TestStrategy()
        {
            var java = new JavaHelloWorldStrategy();
            Assert.Equal("Hello Strategy!", java.HelloWorld());
        }
    }
}