using Xunit;

namespace HelloDesignPattern.Tests.structural.facade
{
    public class HelloWorldFacadeTest
    {
        [Fact]
        public void TestHelloWorldFacade()
        {
            IHelloWorld facadeHelloWorld = HelloWorldFacade.Instance().FacadeHelloWorld();
            Assert.Equal("Hello Facade!", facadeHelloWorld.HelloWorld());
        }
    }
}