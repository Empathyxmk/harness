using Xunit;
using BlackObfuscatorASPlugin;

namespace BlackObfuscatorASPlugin.PublicTests
{
    public class AbxPublicTests
    {
        [Fact]
        public void TestAddDifferentValues()
        {
            Assert.Equal(13, Abx.Add(7, 6));
            Assert.Equal(0, Abx.Add(-3, 3));
        }

        [Fact]
        public void TestIsPositiveDifferentData()
        {
            Assert.True(Abx.IsPositive(2024));
            Assert.False(Abx.IsPositive(-2025));
        }
    }
}