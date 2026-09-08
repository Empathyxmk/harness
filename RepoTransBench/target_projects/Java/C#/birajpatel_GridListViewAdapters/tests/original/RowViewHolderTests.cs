using System;
using Xunit;
using System.Collections.Generic;

namespace GridListViewAdapters.Tests
{
    public class RowViewHolderTests
    {
        [Fact]
        public void GetCardViewHolders_InitialEmpty()
        {
            var holder = new RowViewHolder<string>();
            List<string> l = holder.GetCardViewHolders();
            Assert.NotNull(l);
            Assert.Empty(l);
        }

        [Fact]
        public void AddItemToCardViewHolders()
        {
            var holder = new RowViewHolder<string>();
            holder.GetCardViewHolders().Add("abc");
            Assert.Single(holder.GetCardViewHolders());
            Assert.Equal("abc", holder.GetCardViewHolders()[0]);
        }
    }
}