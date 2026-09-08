using Xunit;

namespace WoodpeckerYsoserial.PublicTests
{
    public class YsoConfigSmokePublicTest
    {
        [Fact]
        public void TestDefaultCompressFlag()
        {
            var config = new YsoConfig();
            Assert.False(config.IsCompress());
        }

        [Fact]
        public void TestSetCompressToTrue()
        {
            var config = new YsoConfig();
            config.SetCompress(true);
            Assert.True(config.IsCompress());
        }

        [Fact]
        public void TestSetCompressToFalse()
        {
            var config = new YsoConfig();
            config.SetCompress(true);
            config.SetCompress(false);
            Assert.False(config.IsCompress());
        }
    }
}