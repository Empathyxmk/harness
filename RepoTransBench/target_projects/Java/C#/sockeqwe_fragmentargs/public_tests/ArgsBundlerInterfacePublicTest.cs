using Xunit;

namespace ProjectName.PublicTests.Bundler
{
    public class Bundle
    {
        private readonly Dictionary<string, string> _stringDict = new();

        public void PutString(string key, string value) => _stringDict[key] = value;
        public string? GetString(string key) => _stringDict.TryGetValue(key, out var v) ? v : null;
    }

    public abstract class ArgsBundler<T>
    {
        public abstract void Put(string key, T value, Bundle bundle);
        public abstract T Get(string key, Bundle bundle);
    }

    public class PublicTestBundler : ArgsBundler<string>
    {
        public override void Put(string key, string value, Bundle bundle)
        {
            bundle.PutString(key, "PUBLIC_" + value + "_PUBTEST");
        }

        public override string Get(string key, Bundle bundle)
        {
            var v = bundle.GetString(key);
            return v == null ? null! : v.Replace("PUBLIC_", "").Replace("_PUBTEST", "");
        }
    }

    public class ArgsBundlerInterfacePublicTest
    {
        [Fact]
        public void InterfacePutAddsPrefixSuffix_Public()
        {
            var bundle = new Bundle();
            new PublicTestBundler().Put("PUBKEY", "valueForPublic", bundle);
            Assert.Equal("PUBLIC_valueForPublic_PUBTEST", bundle.GetString("PUBKEY"));
        }

        [Fact]
        public void InterfaceGetRemovesPrefixSuffix_Public()
        {
            var bundle = new Bundle();
            bundle.PutString("PUB_KEY", "PUBLIC_zxy_PUBTEST");
            Assert.Equal("zxy", new PublicTestBundler().Get("PUB_KEY", bundle));
        }
    }
}