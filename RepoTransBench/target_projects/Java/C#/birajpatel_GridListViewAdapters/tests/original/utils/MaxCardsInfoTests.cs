using Xunit;

namespace GridListViewAdapters.Tests.Utils
{
    public class MaxCardsInfoTests
    {
        [Fact]
        public void Constructor_DoesNotThrow()
        {
            var info = new MaxCardsInfo(4, 3);
        }
    }
}