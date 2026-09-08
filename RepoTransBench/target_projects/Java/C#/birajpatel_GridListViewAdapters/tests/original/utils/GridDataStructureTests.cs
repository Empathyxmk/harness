using Xunit;
using System.Collections.Generic;
using System.Linq;

namespace GridListViewAdapters.Tests.Utils
{
    public class GridDataStructureTests
    {
        private GridDataStructure<string> gridData;

        public GridDataStructureTests()
        {
            var list = new List<string> { "A", "B", "C", "D", "E" };
            gridData = new GridDataStructure<string>(list, 2);
        }

        [Fact]
        public void GetRowCount_ReturnsExpectedValue()
        {
            Assert.Equal(3, gridData.GetRowCount());
        }

        [Fact]
        public void GetDataForRow_ReturnsExpectedRow()
        {
            var row = gridData.GetDataForRow(1);
            Assert.Equal(new List<string> { "C", "D" }, row.ToList());
        }

        [Fact]
        public void GetDataForLastRow_ReturnsRemainder()
        {
            var row = gridData.GetDataForRow(2);
            Assert.Equal(new List<string> { "E" }, row.ToList());
        }

        [Fact]
        public void GetDataForRow_InvalidRow_Throws()
        {
            Assert.Throws<System.ArgumentOutOfRangeException>(() => gridData.GetDataForRow(6));
        }
    }
}