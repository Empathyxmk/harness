using Xunit;

namespace WoodpeckerYsoserial.Tests
{
    public class StringsSmokeTest
    {
        [Fact]
        public void TestIsEmpty()
        {
            Assert.True(Strings.IsEmpty(null));
            Assert.True(Strings.IsEmpty(""));
            Assert.False(Strings.IsEmpty("abc"));
        }

        [Fact]
        public void TestIsNotEmpty()
        {
            Assert.False(Strings.IsNotEmpty(null));
            Assert.False(Strings.IsNotEmpty(""));
            Assert.True(Strings.IsNotEmpty("value"));
        }

        [Fact]
        public void TestRepeat()
        {
            Assert.Equal("", Strings.Repeat("x", 0));
            Assert.Equal("xxx", Strings.Repeat("x", 3));
            Assert.Equal("foobarfoobar", Strings.Repeat("foobar", 2));
        }
    }
}