using Xunit;

namespace GridListViewAdapters.Tests.Dataholders
{
    public class CardDataHolderTests
    {
        [Fact]
        public void CardDataHolder_PropertiesMatch()
        {
            var holder = new CardDataHolder("text", 1, 2, false, 0);
            Assert.Equal("text", holder.Text);
            Assert.Equal(1, holder.CardType);
            Assert.Equal(2, holder.Position);
            Assert.False(holder.IsHeaderOrFooter);
            Assert.Equal(0, holder.ViewType);
        }
    }
}