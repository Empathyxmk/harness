using System.Collections.Generic;
using Xunit;
using Moq;
using MarkZhai.DataBindingAdapter;

namespace MarkZhai.DataBindingAdapter.Tests.Original
{
    public class MultiTypeAdapterTest
    {
        private object context;
        private object inflater;

        public MultiTypeAdapterTest()
        {
            context = new object();
            inflater = new object();
        }

        [Fact]
        public void TestAddAndViewType()
        {
            var adapter = new MultiTypeAdapter(context);
            adapter.AddViewTypeToLayoutMap(1, 100);
            adapter.Add("foo", 1);
            Assert.Equal(1, adapter.GetItemCount());
            Assert.Equal(1, adapter.GetItemViewType(0));
        }

        [Fact]
        public void TestAddAllAndSet()
        {
            var adapter = new MultiTypeAdapter(context);
            adapter.AddViewTypeToLayoutMap(8, 108);
            List<object> list = new List<object> { "a", "b" };
            adapter.AddAll(list, 8);
            Assert.Equal(2, adapter.GetItemCount());
            Assert.Equal(8, adapter.GetItemViewType(1));
            adapter.Set(new List<object> { "x", "y" }, 8);
            Assert.Equal(2, adapter.GetItemCount());
            Assert.Equal(8, adapter.GetItemViewType(0));
        }

        [Fact]
        public void TestRemoveClear()
        {
            var adapter = new MultiTypeAdapter(context);
            adapter.AddViewTypeToLayoutMap(2, 102);
            adapter.Add("bar", 2);
            Assert.Equal(1, adapter.GetItemCount());
            adapter.Remove(0);
            Assert.Equal(0, adapter.GetItemCount());
            adapter.Add("foo", 2);
            adapter.Clear();
            Assert.Equal(0, adapter.GetItemCount());
        }

        [Fact]
        public void TestSetWithTyper()
        {
            var typerMock = new Mock<MultiTypeAdapter.MultiViewTyper>();
            typerMock.Setup(t => t.GetViewType(It.IsAny<object>())).Returns(3);
            var adapter = new MultiTypeAdapter(context);
            adapter.AddViewTypeToLayoutMap(3, 103);
            adapter.Set(new List<object> { "f", "g" }, typerMock.Object);
            Assert.Equal(2, adapter.GetItemCount());
            Assert.Equal(3, adapter.GetItemViewType(1));
        }

        [Fact]
        public void TestAddAtPositionAndAddAllPosition()
        {
            var adapter = new MultiTypeAdapter(context);
            adapter.AddViewTypeToLayoutMap(5, 105);
            adapter.Add("m", 5);
            adapter.Add(0, "n", 5);
            List<object> list = new List<object> { "a", "b" };
            adapter.AddAll(0, list, 5);
            Assert.Equal(4, adapter.GetItemCount());
            Assert.Equal(5, adapter.GetItemViewType(2));
        }
    }
}