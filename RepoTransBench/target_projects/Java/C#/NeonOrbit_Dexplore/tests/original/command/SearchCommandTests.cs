using Xunit;
using NeonOrbit.Dexplore.Command;

namespace NeonOrbit.Dexplore.Tests.Command
{
    public class SearchCommandTests
    {
        [Fact]
        public void Should_FindResults_ForExistingTerm()
        {
            // Arrange
            var command = new SearchCommand();
            string term = "MainActivity";

            // Act
            var results = command.Execute(new[] { term });

            // Assert
            Assert.NotNull(results);
            Assert.Contains("MainActivity", results);
        }

        [Fact]
        public void Should_ReturnEmpty_ForMissingTerm()
        {
            // Arrange
            var command = new SearchCommand();
            string term = "ClassThatDoesNotExist";

            // Act
            var results = command.Execute(new[] { term });

            // Assert
            Assert.True(results == null || results.Length == 0 || !results.Contains("ClassThatDoesNotExist"), "Should not find nonexistent class");
        }

        [Fact]
        public void Should_Handle_MultipleSearchTerms()
        {
            // Arrange
            var command = new SearchCommand();
            string[] terms = { "MainActivity", "OtherClass" };

            // Act
            var results = command.Execute(terms);

            // Assert
            Assert.NotNull(results);
            Assert.True(results.Contains("MainActivity") || results.Contains("OtherClass"));
        }
    }
}