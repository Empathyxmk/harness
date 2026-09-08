using Xunit;

namespace HelloDesignPattern.Tests.creational.abstract_factory
{
    public class AbstractFactoryTest
    {
        [Fact]
        public void TestHelloWorld()
        {
            var splitHelloWorldFactory = AbstractFactory.Select(AbstractFactory.Type.Java);
            Assert.Equal("Java", splitHelloWorldFactory.CreateHelloWorldObject().Object());
            Assert.Equal("Hello", splitHelloWorldFactory.CreateHelloWorldInterjection().Interjection());
            splitHelloWorldFactory = AbstractFactory.Select(AbstractFactory.Type.DesignPattern);
            Assert.Equal("Hello", splitHelloWorldFactory.CreateHelloWorldInterjection().Interjection());
            Assert.Equal("Abstract Factory", splitHelloWorldFactory.CreateHelloWorldObject().Object());
        }
    }
}