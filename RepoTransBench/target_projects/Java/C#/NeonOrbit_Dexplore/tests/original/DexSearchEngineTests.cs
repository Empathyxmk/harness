using Xunit;
using NeonOrbit.Dexplore;

namespace NeonOrbit.Dexplore.Tests
{
    public class DexSearchEngineTests
    {
        [Fact]
        public void Should_FindClassNames_When_SearchSimpleClass()
        {
            // Arrange
            var dex = TestUtilities.LoadTestDex();
            var searchEngine = new DexSearchEngine(dex);

            // Act
            var classes = searchEngine.FindClasses("Main");

            // Assert
            Assert.Contains("com.example.MainActivity", classes);
        }

        [Fact]
        public void Should_ReturnEmpty_When_NoMatch()
        {
            // Arrange
            var dex = TestUtilities.LoadTestDex();
            var searchEngine = new DexSearchEngine(dex);

            // Act
            var classes = searchEngine.FindClasses("NoSuchClassName");

            // Assert
            Assert.Empty(classes);
        }

        [Fact]
        public void Should_HandleMultipleQueries()
        {
            // Arrange
            var dex = TestUtilities.LoadTestDex();
            var searchEngine = new DexSearchEngine(dex);

            // Act
            var results = searchEngine.FindClasses("Main", "Example");

            // Assert
            Assert.Contains("com.example.MainActivity", results);
        }
    }
}