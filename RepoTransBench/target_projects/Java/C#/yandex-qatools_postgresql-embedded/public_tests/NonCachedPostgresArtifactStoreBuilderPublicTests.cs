using Xunit;

namespace PublicTests
{
    public class NonCachedPostgresArtifactStoreBuilderPublicTests
    {
        class DummyBuilder
        {
            private string config;
            public DummyBuilder CustomConfig(string config) { this.config = config; return this; }
            public string GetConfig() => config;
        }

        [Fact]
        public void SetsCustomConfigDifferentFromPrivateTest()
        {
            var builder = new DummyBuilder().CustomConfig("public_config_4567");
            Assert.Equal("public_config_4567", builder.GetConfig());
        }

        [Fact]
        public void ConfigIsNullByDefault()
        {
            var builder = new DummyBuilder();
            Assert.Null(builder.GetConfig());
        }
    }
}