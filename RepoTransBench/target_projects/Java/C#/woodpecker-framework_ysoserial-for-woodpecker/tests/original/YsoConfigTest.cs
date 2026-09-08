using Xunit;

namespace WoodpeckerYsoserial.Tests
{
    public class YsoConfigTest
    {
        [Fact]
        public void TestDefaultIsCompressIsFalse()
        {
            var config = new YsoConfig();
            Assert.False(config.IsCompress());
        }

        [Fact]
        public void TestSetCompressTrue()
        {
            var config = new YsoConfig();
            config.SetCompress(true);
            Assert.True(config.IsCompress());
        }

        [Fact]
        public void TestSetCompressFalse()
        {
            var config = new YsoConfig();
            config.SetCompress(true);
            config.SetCompress(false);
            Assert.False(config.IsCompress());
        }
    }
}