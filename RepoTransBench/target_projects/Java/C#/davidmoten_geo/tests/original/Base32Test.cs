using Xunit;

namespace DavidMoten.Geo.Tests
{
    public class Base32Test
    {
        [Fact]
        public void TestEncodeBase32LongPositive()
        {
            long l = 123456789L;
            string encoded = Base32.EncodeBase32(l, 8);
            Assert.NotNull(encoded);
            Assert.Equal(8, encoded.Length);
        }

        [Fact]
        public void TestEncodeBase32LongNegative()
        {
            long l = -987654321L;
            string encoded = Base32.EncodeBase32(l, 10);
            Assert.NotNull(encoded);
            Assert.StartsWith("-", encoded);
            Assert.Equal(11, encoded.Length); // "-" + 10 digits
        }

        [Fact]
        public void TestEncodeBase32DefaultLength()
        {
            string encoded = Base32.EncodeBase32(123);
            Assert.Equal(GeoHash.MAX_HASH_LENGTH, encoded.Length);
        }

        [Fact]
        public void TestDecodeBase32Positive()
        {
            long original = 123456789L;
            string encoded = Base32.EncodeBase32(original, 12);
            long decoded = Base32.DecodeBase32(encoded);
            Assert.Equal(original, decoded);
        }

        [Fact]
        public void TestDecodeBase32Negative()
        {
            long original = -987654321L;
            string encoded = Base32.EncodeBase32(original, 6);
            long decoded = Base32.DecodeBase32(encoded);
            Assert.Equal(original, decoded);
        }

        [Fact]
        public void TestGetCharIndexValid()
        {
            Assert.Equal(1, Base32.GetCharIndex('1'));
            Assert.Equal(10, Base32.GetCharIndex('b'));
            Assert.Equal(31, Base32.GetCharIndex('z'));
        }

        [Fact]
        public void TestGetCharIndexInvalid()
        {
            Assert.Throws<System.ArgumentException>(() => Base32.GetCharIndex('!'));
        }

        [Fact]
        public void TestPadLeftWithZerosToLengthShort()
        {
            string result = Base32.PadLeftWithZerosToLength("abc", 5);
            Assert.Equal("00abc", result);
        }

        [Fact]
        public void TestPadLeftWithZerosToLengthExact()
        {
            string result = Base32.PadLeftWithZerosToLength("abc", 3);
            Assert.Equal("abc", result);
        }
    }
}