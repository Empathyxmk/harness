using Xunit;

namespace GoogleMailImporter.PublicTests.Local.Thunderbird
{
    public class XMozillaStatusPublicTests
    {
        [Fact]
        public void TestParsesDifferentHexString()
        {
            int status = XMozillaStatusParser.ParseXMozillaStatus("0x0018");
            Assert.Equal(0x18, status);
        }

        [Fact]
        public void TestParsesDifferentHexStringZero()
        {
            int status = XMozillaStatusParser.ParseXMozillaStatus("0x0");
            Assert.Equal(0, status);
        }

        [Fact]
        public void TestParsesDifferentHexStringUppercase()
        {
            int status = XMozillaStatusParser.ParseXMozillaStatus("0X0022");
            Assert.Equal(0x22, status);
        }
    }

    public static class XMozillaStatusParser
    {
        public static int ParseXMozillaStatus(string str)
        {
            if (str.StartsWith("0x") || str.StartsWith("0X"))
                return int.Parse(str.Substring(2), System.Globalization.NumberStyles.HexNumber);
            return int.Parse(str);
        }
    }
}