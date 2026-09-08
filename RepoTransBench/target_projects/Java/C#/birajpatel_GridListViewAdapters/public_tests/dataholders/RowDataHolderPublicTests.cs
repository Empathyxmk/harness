using Xunit;

namespace GridListViewAdapters.PublicTests.Dataholders
{
    public class RowDataHolderPublicTests
    {
        [Fact]
        public void SetAndGetRowIdPublic()
        {
            var holder = new RowDataHolder();
            holder.SetRowId(101L);
            Assert.Equal(101L, holder.GetRowId());
        }

        [Fact]
        public void SetAndGetRowPublic()
        {
            var holder = new RowDataHolder();
            object row = "PublicRow";
            holder.SetRow(row);
            Assert.Equal("PublicRow", holder.GetRow());
        }
    }
}