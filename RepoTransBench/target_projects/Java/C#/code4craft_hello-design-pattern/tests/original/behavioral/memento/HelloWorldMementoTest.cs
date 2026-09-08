using Xunit;

namespace HelloDesignPattern.Tests.behavioral.memento
{
    public class HelloWorldMementoTest
    {
        [Fact]
        public void TestHelloWorldMediator()
        {
            var helloWorldMementoOriginator = new HelloWorldMementoOriginator();
            var memento = helloWorldMementoOriginator.Set("Hello Memento!").SaveToMemento();
            helloWorldMementoOriginator.Set("Hello Whatever!");
            Assert.Equal("Hello Whatever!", helloWorldMementoOriginator.HelloWorld());
            helloWorldMementoOriginator.RestoreFromMemento(memento);
            Assert.Equal("Hello Memento!", helloWorldMementoOriginator.HelloWorld());
        }
    }
}