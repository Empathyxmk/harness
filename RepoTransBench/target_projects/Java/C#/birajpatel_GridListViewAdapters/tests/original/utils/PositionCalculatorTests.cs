using Xunit;

namespace GridListViewAdapters.Tests.Utils
{
    public class PositionCalculatorTests
    {
        [Fact]
        public void GetRowAndColumnIndex_ResultIsValid()
        {
            int position = 7, columns = 3;
            var res = PositionCalculator.GetRowAndColumnIndex(position, columns);
            Assert.Equal(new int[] { 2, 1 }, res);
        }

        [Fact]
        public void GetPosition_ReturnsCorrectIndex()
        {
            int row = 2, col = 1, columns = 3;
            int position = PositionCalculator.GetPosition(row, col, columns);
            Assert.Equal(7, position);
        }

        [Fact]
        public void GetTotalRows_ReturnsFloor()
        {
            Assert.Equal(4, PositionCalculator.GetTotalRows(10, 3));
        }
    }
}