using Xunit;

namespace HelloDesignPattern.Tests.structural.adapter
{
    public class HelloWorldAdapterTest
    {
        [Fact]
        public void TestHelloWorldAdapter()
        {
            IHelloWorld adapterHelloWorld = new HelloWorldAdapter(new HelloAdapterDesignPattern());
            Assert.Equal("Hello Adapter!", adapterHelloWorld.HelloWorld());
        }
    }
}