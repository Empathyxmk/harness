using Xunit;

namespace HelloDesignPattern.Tests.creational.prototype
{
    public class HelloWorldPrototypeTest
    {
        [Fact]
        public void TestHelloWorldPrototype()
        {
            IHelloWorld helloWorld = HelloWorldPrototype.PROTOTYPE.Clone();
            Assert.Equal("Hello Prototype!", helloWorld.HelloWorld());
        }
    }
}