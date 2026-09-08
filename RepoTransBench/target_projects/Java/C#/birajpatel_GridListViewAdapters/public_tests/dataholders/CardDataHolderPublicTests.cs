using Xunit;

namespace GridListViewAdapters.PublicTests.Dataholders
{
    public class CardDataHolderPublicTests
    {
        [Fact]
        public void SetAndGetCardIdPublic()
        {
            var holder = new CardDataHolder();
            holder.SetCardId(808L);
            Assert.Equal(808L, holder.GetCardId());
        }

        [Fact]
        public void SetAndGetIsEnabledPublic()
        {
            var holder = new CardDataHolder();
            holder.SetIsEnabled(false);
            Assert.False(holder.IsEnabled());
        }

        [Fact]
        public void SetAndGetCardPublic()
        {
            var holder = new CardDataHolder();
            object card = "testPublicCard";
            holder.SetCard(card);
            Assert.Equal("testPublicCard", holder.GetCard());
        }
    }
}