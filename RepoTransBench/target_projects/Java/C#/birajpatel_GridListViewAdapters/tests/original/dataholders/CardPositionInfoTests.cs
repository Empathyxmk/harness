using Xunit;

namespace GridListViewAdapters.Tests.Dataholders
{
    public class CardPositionInfoTests
    {
        [Fact]
        public void Constructor_DoesNotThrow()
        {
            var info = new CardPositionInfo(0, 0, 0);
        }
    }
}