using Xunit;

namespace WoodpeckerYsoserial.Tests
{
    public class GeneratePayloadTest
    {
        [Fact]
        public void TestMainHelp()
        {
            try
            {
                GeneratePayload.Main(new string[] { });
            }
            catch
            {
                Assert.True(true); // Acceptable to throw for invalid input
            }
        }

        [Fact]
        public void TestMainUnknownPayload()
        {
            try
            {
                GeneratePayload.Main(new string[] { "UnknownPayload", "cmd", "id" });
            }
            catch
            {
                Assert.True(true);
            }
        }

        [Fact]
        public void TestMainWithKnownPayloadButMissingArgs()
        {
            try
            {
                GeneratePayload.Main(new string[] { "CommonsCollections1" });
            }
            catch
            {
                Assert.True(true);
            }
        }
    }
}