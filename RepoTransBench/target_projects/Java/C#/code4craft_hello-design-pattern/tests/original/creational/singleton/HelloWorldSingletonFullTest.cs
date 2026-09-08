using Xunit;

namespace HelloDesignPattern.Tests.creational.singleton
{
    public class HelloWorldSingletonFullTest
    {
        [Fact]
        public void TestSingletonInstance_ReturnsSameInstance()
        {
            var instance1 = HelloWorldSingleton.Instance();
            var instance2 = HelloWorldSingleton.Instance();
            Assert.Same(instance1, instance2);
        }

        [Fact]
        public void TestSingletonMessage()
        {
            Assert.Equal("Hello Singleton!", HelloWorldSingleton.Instance().HelloWorld());
        }
    }
}