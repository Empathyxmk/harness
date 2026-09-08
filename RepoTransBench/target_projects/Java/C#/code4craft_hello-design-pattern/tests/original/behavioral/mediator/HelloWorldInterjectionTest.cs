using Xunit;

namespace HelloDesignPattern.Tests.behavioral.mediator
{
    public class HelloWorldInterjectionTest
    {
        [Fact]
        public void TestDefaultConstructorAndSetter()
        {
            var inter = new HelloWorldInterjection();
            Assert.NotNull(inter);
        }
    }
}