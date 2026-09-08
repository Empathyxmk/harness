using Xunit;

namespace GridListViewAdapters.PublicTests.Utils
{
    public class PositionCalculatorPublicTests
    {
        [Fact]
        public void CalculateRowIndexPublic()
        {
            Assert.Equal(2, PositionCalculator.CalculateRowIndex(10, 4));
        }

        [Fact]
        public void CalculateColumnIndexPublic()
        {
            Assert.Equal(3, PositionCalculator.CalculateColumnIndex(7, 4));
        }
    }
}