using Xunit;

namespace HelloDesignPattern.Tests
{
    public class HelloWorldTest
    {
        class Impl : IHelloWorld
        {
            public string HelloWorld() => "custom";
        }

        [Fact]
        public void TestHelloWorldInterfaceImpl()
        {
            IHelloWorld hw = new Impl();
            Assert.Equal("custom", hw.HelloWorld());
        }
    }
}