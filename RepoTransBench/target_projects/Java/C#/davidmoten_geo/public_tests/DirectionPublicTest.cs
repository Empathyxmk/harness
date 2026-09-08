using Xunit;

namespace DavidMoten.Geo.PublicTests
{
    public class DirectionPublicTest
    {
        [Fact]
        public void TestOppositeDifferentOrder()
        {
            Assert.Equal(Direction.LEFT, Direction.RIGHT.Opposite());
            Assert.Equal(Direction.RIGHT, Direction.LEFT.Opposite());
            Assert.Equal(Direction.BOTTOM, Direction.TOP.Opposite());
            Assert.Equal(Direction.TOP, Direction.BOTTOM.Opposite());
        }
    }
}