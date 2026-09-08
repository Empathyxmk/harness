using Xunit;

namespace DavidMoten.Geo.PublicTests
{
    public class Base32PublicTest
    {
        [Fact]
        public void TestEncodeBase32DifferentValue()
        {
            Assert.Equal("1y2p0ij32e8e", Base32.EncodeBase32(1234567890123456L, 12));
        }

        [Fact]
        public void TestDecodeBase32DifferentValue()
        {
            Assert.Equal(123456789L, Base32.DecodeBase32("1ly7vk"));
        }

        [Fact]
        public void TestPadLeftWithZerosToLengthPublic()
        {
            Assert.Equal("00000123", Base32.PadLeftWithZerosToLength("123", 8));
        }

        [Fact]
        public void TestGetCharIndexDifferentChar()
        {
            Assert.Equal(21, Base32.GetCharIndex('q'));
        }
    }
}