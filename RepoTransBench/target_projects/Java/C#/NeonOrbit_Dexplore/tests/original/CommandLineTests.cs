using Xunit;
using NeonOrbit.Dexplore;
using System;

namespace NeonOrbit.Dexplore.Tests
{
    public class CommandLineTests
    {
        [Fact]
        public void Should_ReturnHelp_When_HelpArgumentProvided()
        {
            // Arrange
            string[] args = new[] { "--help" };

            // Act
            var output = CommandLine.Run(args);

            // Assert
            Assert.Contains("Usage:", output, StringComparison.OrdinalIgnoreCase);
        }

        [Fact]
        public void Should_Error_When_InvalidArgumentProvided()
        {
            // Arrange
            string[] args = new[] { "--notARealFlag" };

            // Act & Assert
            var ex = Assert.Throws<ArgumentException>(() => CommandLine.Run(args));
            Assert.Contains("Unknown argument", ex.Message, StringComparison.OrdinalIgnoreCase);
        }
    }
}