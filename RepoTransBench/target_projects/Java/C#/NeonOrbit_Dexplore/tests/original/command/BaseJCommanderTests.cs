using Xunit;
using NeonOrbit.Dexplore.Command;
using System;

namespace NeonOrbit.Dexplore.Tests.Command
{
    public class BaseJCommanderTests
    {
        [Fact]
        public void Should_ParseCommandOptions()
        {
            // Arrange
            var args = new[] { "-v", "--config", "myconfig.json" };
            var parser = new BaseJCommander();

            // Act
            parser.Parse(args);

            // Assert
            Assert.True(parser.VerboseMode);
            Assert.Equal("myconfig.json", parser.ConfigPath);
        }

        [Fact]
        public void Should_FailForInvalidArgs()
        {
            // Arrange
            var args = new[] { "--badflag" };
            var parser = new BaseJCommander();

            // Act & Assert
            Assert.Throws<ArgumentException>(() => parser.Parse(args));
        }
    }
}