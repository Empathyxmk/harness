using Xunit;

namespace GridListViewAdapters.PublicTests.Dataholders
{
    public class CardPositionInfoPublicTests
    {
        [Fact]
        public void SetAndGetRowAndColumnPublic()
        {
            var info = new CardPositionInfo();
            info.SetRow(7);
            info.SetColumn(8);
            Assert.Equal(7, info.GetRow());
            Assert.Equal(8, info.GetColumn());
        }
    }
}