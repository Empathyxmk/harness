using Xunit;

namespace OriginalTests
{
    public class EmbeddedPostgresTests
    {
        class EmbeddedPostgres
        {
            private bool running = false;
            public void Start() { running = true; }
            public void Stop() { running = false; }
            public bool IsRunning() => running;
        }

        [Fact]
        public void StartsAndStops()
        {
            var pg = new EmbeddedPostgres();
            Assert.False(pg.IsRunning());
            pg.Start();
            Assert.True(pg.IsRunning());
            pg.Stop();
            Assert.False(pg.IsRunning());
        }
    }
}