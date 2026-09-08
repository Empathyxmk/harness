using Xunit;
using NeonOrbit.Dexplore.Decompiler;
using System.IO;

namespace NeonOrbit.Dexplore.Tests.Decompiler
{
    public class DexDecompilerTests
    {
        [Fact]
        public void Should_DecompileDexFile_ToSmali()
        {
            // Arrange
            var decompiler = new DexDecompiler();
            string dexPath = TestUtilities.GetSampleDexFile();

            // Act
            string smali = decompiler.Decompile(dexPath);

            // Assert
            Assert.NotNull(smali);
            Assert.Contains(".class", smali);
        }

        [Fact]
        public void ShouldRaise_When_FileDoesNotExist()
        {
            // Arrange
            var decompiler = new DexDecompiler();
            string dexPath = "notfound.dex";

            // Act & Assert
            Assert.Throws<FileNotFoundException>(() => decompiler.Decompile(dexPath));
        }
    }
}