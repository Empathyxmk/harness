using Xunit;

namespace DavidMoten.Geo.Tests
{
    public class DirectionTest
    {
        [Fact]
        public void TestOpposite()
        {
            Assert.Equal(Direction.TOP, Direction.BOTTOM.Opposite());
            Assert.Equal(Direction.BOTTOM, Direction.TOP.Opposite());
            Assert.Equal(Direction.RIGHT, Direction.LEFT.Opposite());
            Assert.Equal(Direction.LEFT, Direction.RIGHT.Opposite());
        }
    }
}