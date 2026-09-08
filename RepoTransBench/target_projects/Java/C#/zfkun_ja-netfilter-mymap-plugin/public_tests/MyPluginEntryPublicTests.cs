using Xunit;
using zfkun_ja_netfilter_mymap_plugin;
using zfkun_ja_netfilter_mymap_plugin.Core;

namespace zfkun_ja_netfilter_mymap_plugin.PublicTests
{
    public class MyPluginEntryPublicTests
    {
        [Fact]
        public void TestInitAndGetters_Public()
        {
            var entry = new MyPluginEntry();
            entry.Init(null, new PluginConfig());
            Assert.NotNull(entry.GetTransformers());
        }

        [Fact]
        public void TestMeta_Public()
        {
            var entry = new MyPluginEntry();
            Assert.Equal("MyMapPlugin", entry.GetName());
            Assert.Equal("zfkun", entry.GetAuthor());
            Assert.Equal("1.0.0", entry.GetVersion());
            Assert.Contains("plugin", entry.GetDescription().ToLower());
        }
    }
}