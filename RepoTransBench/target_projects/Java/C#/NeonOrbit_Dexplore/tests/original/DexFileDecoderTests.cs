using Xunit;
using NeonOrbit.Dexplore;
using System;
using System.IO;

namespace NeonOrbit.Dexplore.Tests
{
    public class DexFileDecoderTests
    {
        [Fact]
        public void Should_ThrowException_When_FileNotFound()
        {
            // Arrange
            string fakeFilePath = "nonexistent.dex";

            // Act & Assert
            Assert.Throws<FileNotFoundException>(() => DexFileDecoder.Decode(fakeFilePath));
        }

        [Fact]
        public void Should_DecodeFileCorrectly_When_ValidDex()
        {
            // Arrange
            string sampleDexPath = TestUtilities.GetSampleDexFile();

            // Act
            var result = DexFileDecoder.Decode(sampleDexPath);

            // Assert
            Assert.NotNull(result);
            Assert.True(result.MethodCount > 0, "Decoded dex should have at least 1 method.");
        }
    }
}