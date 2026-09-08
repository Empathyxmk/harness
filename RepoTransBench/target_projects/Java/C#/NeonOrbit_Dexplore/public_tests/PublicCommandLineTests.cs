using Xunit;
using NeonOrbit.Dexplore;

namespace NeonOrbit.Dexplore.PublicTests
{
    public class PublicCommandLineTests
    {
        [Fact]
        public void Should_ReturnUsage_When_EmptyArgs()
        {
            // Arrange
            string[] args = new string[0];

            // Act
            var output = CommandLine.Run(args);

            // Assert
            Assert.Contains("Usage", output);
        }
    }
}