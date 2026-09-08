using Xunit;

namespace HelloDesignPattern.Tests.structural.flyweight
{
    public class HelloWorldFlyWeightTest
    {
        [Fact]
        public void TestHelloWorldFlyWeight()
        {
            var helloWorld1 = HelloWorldFlyWeightFactory.Instance().CreateHelloWorld("Hello Flyweight!");
            Assert.Equal("Hello Flyweight!", helloWorld1.HelloWorld());
            var helloWorld2 = HelloWorldFlyWeightFactory.Instance().CreateHelloWorld("Hello Flyweight!");
            Assert.Equal("Hello Flyweight!", helloWorld2.HelloWorld());
        }
    }
}