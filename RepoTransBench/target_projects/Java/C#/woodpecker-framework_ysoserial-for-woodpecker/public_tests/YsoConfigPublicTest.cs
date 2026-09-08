using Xunit;

namespace WoodpeckerYsoserial.PublicTests
{
    public class YsoConfigPublicTest
    {
        [Fact]
        public void TestCompressFlagToggle()
        {
            var config = new YsoConfig();
            Assert.False(config.IsCompress());
            config.SetCompress(true);
            Assert.True(config.IsCompress());
            config.SetCompress(false);
            Assert.False(config.IsCompress());
        }

        [Fact]
        public void TestMultipleToggles()
        {
            var config = new YsoConfig();
            config.SetCompress(true);
            config.SetCompress(true);
            Assert.True(config.IsCompress());
            config.SetCompress(false);
            Assert.False(config.IsCompress());
            config.SetCompress(true);
            Assert.True(config.IsCompress());
        }
    }
}