using Xunit;
using NeonOrbit.Dexplore.Command;
using System;

namespace NeonOrbit.Dexplore.Tests.Command
{
    public class DecodeCommandTests
    {
        [Fact]
        public void Should_DecodeDex_Successfully()
        {
            // Arrange
            var command = new DecodeCommand();
            string dexPath = TestUtilities.GetSampleDexFile();

            // Act
            var result = command.Execute(new[] { dexPath });

            // Assert
            Assert.NotNull(result);
            Assert.Contains("Classes:", result);
        }

        [Fact]
        public void Should_ReportError_If_FileMissing()
        {
            // Arrange
            var command = new DecodeCommand();

            // Act & Assert
            var ex = Assert.Throws<FileNotFoundException>(() => command.Execute(new[] { "missing.dex" }));
            Assert.Contains("not found", ex.Message, StringComparison.OrdinalIgnoreCase);
        }
    }
}