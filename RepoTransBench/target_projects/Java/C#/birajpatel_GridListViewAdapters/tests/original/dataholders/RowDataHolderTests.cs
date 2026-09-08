using Xunit;

namespace GridListViewAdapters.Tests.Dataholders
{
    public class RowDataHolderTests
    {
        [Fact]
        public void RowDataHolder_PropertiesMatch()
        {
            var holder = new RowDataHolder(0, 1);
            Assert.Equal(0, holder.RowNum);
            Assert.Equal(1, holder.NumOfColumns);
        }
    }
}