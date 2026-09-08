using Xunit;

namespace OriginalTests
{
    public class TestPostgresStarterTests
    {
        class DummyStarter
        {
            private bool started = false;
            public void Start() { started = true; }
            public void Stop() { started = false; }
            public bool IsStarted() => started;
        }

        [Fact]
        public void StartSetsFlag()
        {
            var starter = new DummyStarter();
            Assert.False(starter.IsStarted());
            starter.Start();
            Assert.True(starter.IsStarted());
        }

        [Fact]
        public void StopResetsFlag()
        {
            var starter = new DummyStarter();
            starter.Start();
            starter.Stop();
            Assert.False(starter.IsStarted());
        }
    }
}