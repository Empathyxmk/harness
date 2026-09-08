using Xunit;

namespace GridListViewAdapters.PublicTests.Utils
{
    public class MaxCardsInfoPublicTests
    {
        [Fact]
        public void SetAndGetMaxCardsPerRowPublic()
        {
            var info = new MaxCardsInfo();
            info.SetMaxCardsPerRow(6);
            Assert.Equal(6, info.GetMaxCardsPerRow());
        }
    }
}