using Xunit;
using Moq;
using System.IO;

namespace HelloDesignPattern.Tests.behavioral.observer
{
    public class HelloWorldObserverTest
    {
        [Fact]
        public void TestHelloWorldObserver()
        {
            var observer = new HelloWorldObserver();
            var mockPrinter = new Mock<TextWriter>();
            observer.SetPrinter(mockPrinter.Object);
            var subject = new Subject().Attach(observer);
            subject.NotifyObservers();
            mockPrinter.Verify(writer => writer.WriteLine("Hello Observer!"), Times.Once());
        }
    }
}