using Xunit;

namespace GridListViewAdapters.PublicTests.Utils
{
    public class GridDataStructurePublicTests
    {
        [Fact]
        public void GetSetItemPublic()
        {
            var grid = new GridDataStructure<string>(3, 3);
            grid.SetItem(2, 1, "GridTest");
            Assert.Equal("GridTest", grid.GetItem(2, 1));
        }

        [Fact]
        public void GetNumRowsColsPublic()
        {
            var grid = new GridDataStructure<string>(2, 5);
            Assert.Equal(2, grid.GetNumRows());
            Assert.Equal(5, grid.GetNumColumns());
        }
    }
}