using Xunit;

namespace HelloDesignPattern.Tests.structural.bridge
{
    public class HelloWorldBridgeTest
    {
        [Fact]
        public void TestHelloWorldAdapter()
        {
            IHelloWorld bridgeHelloWorld = new HelloWorldBridge(new JavaHelloWorldImpl());
            Assert.Equal("Hello Java!", bridgeHelloWorld.HelloWorld());
            bridgeHelloWorld = new HelloWorldBridge(new DesignPatternWorldImpl());
            Assert.Equal("Hello Bridge!", bridgeHelloWorld.HelloWorld());
        }
    }
}