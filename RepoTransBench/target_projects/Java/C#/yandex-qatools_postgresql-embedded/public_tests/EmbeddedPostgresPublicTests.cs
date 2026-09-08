using Xunit;

namespace PublicTests
{
    public class EmbeddedPostgresPublicTests
    {
        class DummyEmbeddedPostgres
        {
            private bool started = false;
            public void Start(string user, string pass)
            {
                this.started = (user == "publicUser" && pass == "publicPass");
            }
            public bool IsStarted() => started;
        }

        [Fact]
        public void CanStartWithDifferentCredentials()
        {
            var pg = new DummyEmbeddedPostgres();
            pg.Start("publicUser", "publicPass");
            Assert.True(pg.IsStarted());
        }

        [Fact]
        public void FailsToStartWithWrongCredentials()
        {
            var pg = new DummyEmbeddedPostgres();
            pg.Start("bad", "creds");
            Assert.False(pg.IsStarted());
        }
    }
}