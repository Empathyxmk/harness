using Xunit;
using NeonOrbit.Dexplore.Command;

namespace NeonOrbit.Dexplore.PublicTests
{
    public class PublicDecodeCommandTests
    {
        [Fact]
        public void Should_OutputClasses_When_ValidDex()
        {
            // Arrange
            var decodeCmd = new DecodeCommand();
            string dexPath = TestUtilities.GetSampleDexFile();

            // Act
            var output = decodeCmd.Execute(new[] { dexPath });

            // Assert
            Assert.Contains("Classes:", output);
        }

        [Fact]
        public void Should_ReportError_ForInvalidFile()
        {
            // Arrange
            var decodeCmd = new DecodeCommand();

            // Act & Assert
            var ex = Assert.Throws<System.IO.FileNotFoundException>(() => decodeCmd.Execute(new[] { "fakepath.dex" }));
            Assert.Contains("not found", ex.Message, System.StringComparison.OrdinalIgnoreCase);
        }
    }
}