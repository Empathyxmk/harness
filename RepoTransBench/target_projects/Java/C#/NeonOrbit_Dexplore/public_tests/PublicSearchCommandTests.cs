using Xunit;
using NeonOrbit.Dexplore.Command;

namespace NeonOrbit.Dexplore.PublicTests
{
    public class PublicSearchCommandTests
    {
        [Fact]
        public void Should_FindClass_For_PublicSearch()
        {
            // Arrange
            var searchCmd = new SearchCommand();

            // Act
            var result = searchCmd.Execute(new[] { "MainActivity" });

            // Assert
            Assert.NotNull(result);
            Assert.Contains("MainActivity", result);
        }
    }
}