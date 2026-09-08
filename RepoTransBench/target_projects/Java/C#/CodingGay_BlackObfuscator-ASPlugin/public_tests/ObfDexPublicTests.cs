using Xunit;
using BlackObfuscatorASPlugin.Models;

namespace BlackObfuscatorASPlugin.PublicTests
{
    public class ObfDexPublicTests
    {
        [Fact]
        public void TestIsObfuscatedWithDifferentData()
        {
            Assert.False(ObfDex.IsObfuscated("barBazNew"));
            Assert.True(ObfDex.IsObfuscated("obf_PUBLIC_2024"));
        }

        [Fact]
        public void TestObfuscateDifferentData()
        {
            string original = "differentString2024";
            string obfuscated = ObfDex.Obfuscate(original);
            Assert.NotNull(obfuscated);
            Assert.NotEqual(original, obfuscated);
            Assert.Contains("obf", obfuscated);
        }
    }
}