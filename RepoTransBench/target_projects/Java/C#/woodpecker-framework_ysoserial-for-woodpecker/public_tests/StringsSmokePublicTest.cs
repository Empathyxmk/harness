using Xunit;

namespace WoodpeckerYsoserial.PublicTests
{
    public class StringsSmokePublicTest
    {
        [Fact]
        public void TestIsEmptySmokeVariants()
        {
            Assert.True(Strings.IsEmpty(null));
            Assert.True(Strings.IsEmpty(""));
            Assert.False(Strings.IsEmpty("null"));
            Assert.False(Strings.IsEmpty("something"));
        }

        [Fact]
        public void TestIsNotEmptySmokeVariants()
        {
            Assert.False(Strings.IsNotEmpty(null));
            Assert.False(Strings.IsNotEmpty(""));
            Assert.True(Strings.IsNotEmpty("123"));
            Assert.True(Strings.IsNotEmpty("xyz"));
        }

        [Fact]
        public void TestRepeatSmokeVariants()
        {
            Assert.Equal("", Strings.Repeat("a", 0));
            Assert.Equal("zz", Strings.Repeat("z", 2));
            Assert.Equal("PQRPQRPQR", Strings.Repeat("PQR", 3));
        }
    }
}