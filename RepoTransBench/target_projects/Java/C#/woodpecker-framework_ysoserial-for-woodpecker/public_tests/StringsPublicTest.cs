using Xunit;

namespace WoodpeckerYsoserial.PublicTests
{
    public class StringsPublicTest
    {
        [Fact]
        public void TestIsEmpty()
        {
            Assert.True(Strings.IsEmpty(null));
            Assert.True(Strings.IsEmpty(""));
            Assert.False(Strings.IsEmpty(" "));
            Assert.False(Strings.IsEmpty("测试"));
        }

        [Fact]
        public void TestIsNotEmpty()
        {
            Assert.False(Strings.IsNotEmpty(null));
            Assert.False(Strings.IsNotEmpty(""));
            Assert.True(Strings.IsNotEmpty("something"));
            Assert.True(Strings.IsNotEmpty("1"));
        }

        [Fact]
        public void TestRepeat()
        {
            Assert.Equal("", Strings.Repeat("y", 0));
            Assert.Equal("yyyy", Strings.Repeat("y", 4));
            Assert.Equal("helloworldhelloworldhelloworld", Strings.Repeat("helloworld", 3));
        }
    }
}