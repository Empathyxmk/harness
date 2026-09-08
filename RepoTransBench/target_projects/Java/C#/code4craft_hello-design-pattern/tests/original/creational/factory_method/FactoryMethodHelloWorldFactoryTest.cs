using Xunit;

namespace HelloDesignPattern.Tests.creational.factory_method
{
    public class FactoryMethodHelloWorldFactoryTest
    {
        [Fact]
        public void TestFactoryMethodHelloWorldFactory()
        {
            var helloWorldFactory = new HelloWorldFactory();
            IHelloWorld helloWorld = helloWorldFactory.CreateHelloWorld();
            Assert.Equal("Hello World!", helloWorld.HelloWorld());
            var factoryMethodHelloWorldFactory = new FactoryMethodHelloWorldFactory();
            helloWorld = factoryMethodHelloWorldFactory.CreateHelloWorld();
            Assert.Equal("Hello Factory Method!", helloWorld.HelloWorld());
        }
    }
}