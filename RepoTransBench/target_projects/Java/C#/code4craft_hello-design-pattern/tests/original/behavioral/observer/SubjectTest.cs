using Xunit;

namespace HelloDesignPattern.Tests.behavioral.observer
{
    public class SubjectTest
    {
        class DummyObserver : IObserver
        {
            public bool Updated { get; private set; }
            public void Update()
            {
                Updated = true;
            }
        }

        [Fact]
        public void TestAttachAndNotify()
        {
            var subject = new Subject();
            var obs = new DummyObserver();
            subject.Attach(obs);
            subject.NotifyObservers();
            Assert.True(obs.Updated);
        }
    }
}