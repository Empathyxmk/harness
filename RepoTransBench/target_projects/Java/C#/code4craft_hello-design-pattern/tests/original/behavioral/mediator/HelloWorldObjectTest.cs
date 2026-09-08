using Xunit;

namespace HelloDesignPattern.Tests.behavioral.mediator
{
    public class HelloWorldObjectTest
    {
        [Fact]
        public void TestDefaultConstructor()
        {
            var obj = new HelloWorldObject();
            Assert.NotNull(obj);
        }
    }
}