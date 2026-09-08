using Xunit;

namespace HelloDesignPattern.Tests.creational.builder
{
    public class HelloWorldBuilderTest
    {
        [Fact]
        public void TestHelloWorldBuilder()
        {
            var builderHelloWorld = HelloWorldBuilder.Builder()
                .Interjection("Hello")
                .Object("Builder")
                .GetHelloWorld();
            Assert.Equal("Hello Builder!", builderHelloWorld.HelloWorld());

            var helloWorld = HelloWorldBuilder.Builder()
                .Interjection("Hello")
                .Object("World")
                .GetHelloWorld();
            Assert.Equal("Hello World!", helloWorld.HelloWorld());
        }
    }
}