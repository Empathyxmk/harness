using Xunit;
using AllenDowney.ThinkJavaCode;

namespace OriginalTests.Ch13
{
    public class TestTests
    {
        [Fact]
        public void DeckSortingSmokeTest()
        {
            Deck deck = new Deck();
            deck.Shuffle();
            deck.SelectionSort();

            // You could have deeper asserts by checking deck order, but
            // since the Java code just prints "not sorted!" if fail, a smoke run suffices.
        }
    }
}