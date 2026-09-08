using Xunit;

namespace WoodpeckerYsoserial.PublicTests
{
    public class GeneratePayloadPublicTest
    {
        [Fact]
        public void TestYsoConfigCompress()
        {
            // Changing compress state with different sequence
            GeneratePayload.ysoConfig.SetCompress(true);
            Assert.True(GeneratePayload.ysoConfig.IsCompress());
            GeneratePayload.ysoConfig.SetCompress(false);
            Assert.False(GeneratePayload.ysoConfig.IsCompress());
            GeneratePayload.ysoConfig.SetCompress(true);
            Assert.True(GeneratePayload.ysoConfig.IsCompress());
        }
    }
}