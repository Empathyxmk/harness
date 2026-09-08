using System.Collections.Generic;
using Xunit;

namespace GridListViewAdapters.PublicTests
{
    public class RowViewHolderPublicTests
    {
        [Fact]
        public void GetCardViewHoldersInitialEmptyPublic()
        {
            var holder = new RowViewHolder<int>();
            List<int> l = holder.GetCardViewHolders();
            Assert.NotNull(l);
            Assert.Empty(l);
        }

        [Fact]
        public void AddItemToCardViewHoldersPublic()
        {
            var holder = new RowViewHolder<int>();
            holder.GetCardViewHolders().Add(12345);
            Assert.Single(holder.GetCardViewHolders());
            Assert.Equal(12345, holder.GetCardViewHolders()[0]);
        }
    }
}