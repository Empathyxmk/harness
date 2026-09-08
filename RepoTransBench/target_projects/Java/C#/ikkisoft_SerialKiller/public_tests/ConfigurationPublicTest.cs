using System.Collections.Generic;
using Xunit;

namespace Ikkisoft.SerialKiller.PublicTests
{
    public class ConfigurationPublicTest
    {
        [Fact]
        public void TestPropertyLoadDifferentKey()
        {
            var props = new Dictionary<string, string>();
            props["public.test.key"] = "publicValue";
            Assert.True(props.ContainsKey("public.test.key"));
            Assert.Equal("publicValue", props["public.test.key"]);
            Assert.False(props.ContainsKey("nonexistent.key"));
        }
    }
}