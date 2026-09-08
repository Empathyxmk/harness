using Xunit;

namespace GoogleMailImporter.Tests.Original.Local.Thunderbird
{
    public class XMozillaStatusTests
    {
        [Fact]
        public void ParsesHexString()
        {
            int status = XMozillaStatusParser.ParseXMozillaStatus("0x0008");
            Assert.Equal(0x8, status);
        }

        [Fact]
        public void ParsesHexStringZero()
        {
            int status = XMozillaStatusParser.ParseXMozillaStatus("0x0");
            Assert.Equal(0, status);
        }

        [Fact]
        public void ParsesHexStringUppercase()
        {
            int status = XMozillaStatusParser.ParseXMozillaStatus("0X001F");
            Assert.Equal(0x1F, status);
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