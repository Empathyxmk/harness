using Xunit;

namespace HelloDesignPattern.Tests.behavioral.mediator
{
    public class HelloWorldMediatorTest
    {
        [Fact]
        public void TestHelloWorldMediator()
        {
            var helloWorldInterjection = new HelloWorldInterjection();
            var helloWorldObject = new HelloWorldObject();
            var helloWorldMediator = new HelloWorldMediator(helloWorldInterjection, helloWorldObject);
            helloWorldInterjection.SetHelloWorldMediator(helloWorldMediator);
            helloWorldObject.SetHelloWorldMediator(helloWorldMediator);
            Assert.Equal("Hello Mediator!", helloWorldInterjection.HelloWorld());
            Assert.Equal("Hello Mediator!", helloWorldObject.HelloWorld());
        }
    }
}