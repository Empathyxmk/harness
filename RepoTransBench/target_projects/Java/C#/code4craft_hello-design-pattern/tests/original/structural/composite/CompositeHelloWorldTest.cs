using Xunit;

namespace HelloDesignPattern.Tests.structural.composite
{
    public class CompositeHelloWorldTest
    {
        [Fact]
        public void TestCompositeHelloWorld()
        {
            IHelloWorld emptyCompositeHelloWorld = new CompositeHelloWorld();
            Assert.Equal(string.Empty, emptyCompositeHelloWorld.HelloWorld());

            IHelloWorld compositeHelloWorld = new CompositeHelloWorld(new CompositeHelloWorld.DefaultHelloWorld());
            Assert.Equal("Hello Composite!", compositeHelloWorld.HelloWorld());
        }
    }
}