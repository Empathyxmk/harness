using Xunit;
using AllenDowney.ThinkJavaCode;

namespace OriginalTests.Ch14
{
    public class TestTests
    {
        [Fact]
        public void DeckDealSmokeTest()
        {
            Deck deck = new Deck("Deck");
            deck.Shuffle();
            Hand hand = new Hand("Hand");
            deck.Deal(hand, 5);
            hand.Display();

            Hand drawPile = new Hand("Draw Pile");
            deck.DealAll(drawPile);

            // Check that drawPile has expected number of cards (if API available)
            int size = drawPile.Size();
        }
    }
}