using Xunit;

namespace GridListViewAdapters.PublicTests
{
    public class CardPublicTests
    {
        [Fact]
        public void SetAndGetIdPublic()
        {
            var card = new Card();
            card.SetId(99L);
            Assert.Equal(99L, card.GetId());
        }

        [Fact]
        public void SetAndGetIsEnabledPublic()
        {
            var card = new Card();
            card.SetIsEnabled(false);
            Assert.False(card.IsEnabled());
        }

        [Fact]
        public void SetAndGetItemPublic()
        {
            var card = new Card();
            object item = "publicTestObject";
            card.SetItem(item);
            Assert.Equal("publicTestObject", card.GetItem());
        }
    }
}