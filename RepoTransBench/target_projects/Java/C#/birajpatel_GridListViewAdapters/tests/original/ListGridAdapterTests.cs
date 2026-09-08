using System;
using System.Collections.Generic;
using Xunit;
using Moq;

namespace GridListViewAdapters.Tests
{
    public class ListGridAdapterTests
    {
        private ListGridAdapter<string> adapter;
        private List<string> list;

        public ListGridAdapterTests()
        {
            list = new List<string> { "A", "B", "C", "D", "E" };
            adapter = new ListGridAdapter<string>(list, 2);
        }

        [Fact]
        public void GetCount_ReturnsCorrectRows()
        {
            Assert.Equal(3, adapter.GetCount());
        }

        [Fact]
        public void GetItem_ReturnsValue()
        {
            Assert.Equal(list, adapter.GetItem(0));
        }

        [Fact]
        public void GetRowPositionInfo_ReturnsCorrectRowIndex()
        {
            var info = adapter.GetRowPositionInfo(1);
            Assert.Equal(2, info.RowIndex);
        }

        [Fact]
        public void GetView_CallsRowViewHolder()
        {
            var parent = new Mock<IViewGroup>();
            var holder = new Mock<IRowViewHolder>();
            var view = new Mock<IView>();

            parent.Setup(p => p.GetContext()).Returns((object)null);
            holder.Setup(h => h.GetView()).Returns(view.Object);

            // forcibly set private field via reflection, if possible
            var rvf = adapter.GetType().GetField("rowViewHolder", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);
            if (rvf != null)
                rvf.SetValue(adapter, holder.Object);

            var result = adapter.GetView(1, null, parent.Object);
            Assert.NotNull(result);
        }

        [Fact]
        public void AreAllItemsEnabled_True()
        {
            Assert.True(adapter.AreAllItemsEnabled());
        }

        [Fact]
        public void IsEnabled_True()
        {
            Assert.True(adapter.IsEnabled(0));
        }

        [Fact]
        public void GetItem_InvalidIndex_Throws()
        {
            Assert.Throws<IndexOutOfRangeException>(() => adapter.GetItem(10));
        }
    }
}