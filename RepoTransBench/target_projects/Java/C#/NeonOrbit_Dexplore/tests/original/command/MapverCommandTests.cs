using Xunit;
using NeonOrbit.Dexplore.Command;

namespace NeonOrbit.Dexplore.Tests.Command
{
    public class MapverCommandTests
    {
        [Fact]
        public void Should_ReturnVersionInfo()
        {
            // Arrange
            var command = new MapverCommand();

            // Act
            var info = command.Execute(new string[] { });

            // Assert
            Assert.Contains("Version:", info);
        }

        [Fact]
        public void Should_Contain_BuildOrCopyrightInfo()
        {
            // Arrange
            var command = new MapverCommand();

            // Act
            var info = command.Execute(new string[] { });

            // Assert
            Assert.True(info.Contains("Copyright") || info.Contains("Build"), "Should contain copyright or build");
        }
    }
}