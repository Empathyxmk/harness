using Xunit;

namespace HelloDesignPattern.Tests.structural.proxy
{
    public class HelloWorldProxyTest
    {
        [Fact]
        public void TestHelloWorldFacade()
        {
            var helloWorldProxy = new HelloWorldProxy(new HelloWorldProxy.DefaultHelloWorld());
            Assert.Equal("Hello Proxy!", helloWorldProxy.HelloWorld());
        }
    }
}