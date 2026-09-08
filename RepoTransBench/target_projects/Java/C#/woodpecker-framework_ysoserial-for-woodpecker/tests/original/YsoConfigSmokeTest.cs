using System;
using Xunit;

namespace WoodpeckerYsoserial.Tests
{
    public class YsoConfigSmokeTest
    {
        [Fact]
        public void TestDefaultConfig()
        {
            var conf = new YsoConfig();
            Assert.NotNull(conf);
            Assert.NotNull(conf.Config);
        }

        [Fact]
        public void TestSetAndGetConfig()
        {
            var conf = new YsoConfig();
            var props = new System.Collections.Specialized.NameValueCollection();
            props.Set("foo", "bar");
            conf.Config = props;
            Assert.Equal("bar", conf.Config["foo"]);
        }

        [Fact]
        public void TestToString()
        {
            var conf = new YsoConfig();
            conf.Config.Set("k", "v");
            Assert.Contains("k", conf.ToString());
            Assert.Contains("v", conf.ToString());
        }
    }
}