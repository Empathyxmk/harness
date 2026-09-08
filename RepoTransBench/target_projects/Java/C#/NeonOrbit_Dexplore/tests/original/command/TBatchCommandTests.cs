using Xunit;
using NeonOrbit.Dexplore.Command;
using System.Linq;
using System;

namespace NeonOrbit.Dexplore.Tests.Command
{
    public class TBatchCommandTests
    {
        [Fact]
        public void Should_ProcessBatchCommands()
        {
            // Arrange
            var command = new TBatchCommand();
            string[] input = { "decode file1.dex", "decode file2.dex" };

            // Act
            var results = command.ExecuteBatch(input);

            // Assert
            Assert.NotNull(results);
            Assert.Equal(input.Length, results.Length);
        }

        [Fact]
        public void Should_ReturnErrors_ForInvalidBatchCommands()
        {
            // Arrange
            var command = new TBatchCommand();
            string[] input = { "invalidop file1.dex", "decode missingfile.dex" };

            // Act
            var results = command.ExecuteBatch(input);

            // Assert
            Assert.Contains(results, r => r.Contains("error", StringComparison.OrdinalIgnoreCase));
        }

        [Fact]
        public void Should_Handle_EmptyBatch()
        {
            // Arrange
            var command = new TBatchCommand();
            string[] input = new string[0];

            // Act
            var results = command.ExecuteBatch(input);

            // Assert
            Assert.NotNull(results);
            Assert.Empty(results);
        }
    }
}