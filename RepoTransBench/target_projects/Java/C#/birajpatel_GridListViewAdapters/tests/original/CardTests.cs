using System;
using Xunit;
using Moq;

namespace GridListViewAdapters.Tests
{
    public class CardTests
    {
        private class DummyVH { }

        [Fact]
        public void CardCreationAndGetters()
        {
            var v = new Mock<IView>().Object;
            var vh = new DummyVH();

            var card = new Card<DummyVH>(v, vh);
            Assert.Same(v, card.GetCardView());
            Assert.Same(vh, card.GetCardViewHolder());
        }
    }
}