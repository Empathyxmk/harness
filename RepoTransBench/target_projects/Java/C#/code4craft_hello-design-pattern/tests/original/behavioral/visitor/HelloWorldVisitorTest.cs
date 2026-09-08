using Xunit;

namespace HelloDesignPattern.Tests.behavioral.visitor
{
    public class HelloWorldVisitorTest
    {
        [Fact]
        public void TestHelloWorldVisitor()
        {
            var helloWorldCharacterElements = new HelloWorldCharacterElements("Hello Visitor!".ToCharArray());
            var helloWorldCharacterVisitor = new HelloWorldCharacterVisitor();
            helloWorldCharacterElements.Accept(helloWorldCharacterVisitor);
            Assert.Equal("Hello Visitor!", helloWorldCharacterVisitor.HelloWorld());
        }
    }
}