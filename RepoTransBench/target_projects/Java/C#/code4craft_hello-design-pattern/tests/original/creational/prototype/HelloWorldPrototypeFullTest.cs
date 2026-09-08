using Xunit;

namespace HelloDesignPattern.Tests.creational.prototype
{
    public class HelloWorldPrototypeFullTest
    {
        [Fact]
        public void TestHelloWorldPrototype_CloneAndMessage()
        {
            var proto = new HelloWorldPrototype("Test Prototype!");
            IHelloWorld cloned = proto.Clone();
            Assert.IsType<HelloWorldPrototype>(cloned);
            Assert.Equal("Test Prototype!", cloned.HelloWorld());
        }

        [Fact]
        public void TestHelloWorldPrototype_Constant()
        {
            Assert.Equal("Hello Prototype!", HelloWorldPrototype.PROTOTYPE.HelloWorld());
            IHelloWorld copy = HelloWorldPrototype.PROTOTYPE.Clone();
            Assert.IsType<HelloWorldPrototype>(copy);
            Assert.Equal("Hello Prototype!", copy.HelloWorld());
        }
    }
}