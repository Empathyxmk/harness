using System.Collections.Generic;
using Xunit;
using Moq;
using MarkZhai.DataBindingAdapter;

namespace MarkZhai.DataBindingAdapter.Tests.Public
{
    public class MultiTypeAdapterPublicTest
    {
        private object context;
        private object inflater;

        public MultiTypeAdapterPublicTest()
        {
            context = new object();
            inflater = new object();
        }

        [Fact]
        public void TestAddAndViewTypePublic()
        {
            var adapter = new MultiTypeAdapter(context);
            adapter.AddViewTypeToLayoutMap(9, 109);
            adapter.Add("baz", 9);
            Assert.Equal(1, adapter.GetItemCount());
            Assert.Equal(9, adapter.GetItemViewType(0));
        }

        [Fact]
        public void TestAddAllAndSetPublic()
        {
            var adapter = new MultiTypeAdapter(context);
            adapter.AddViewTypeToLayoutMap(11, 111);
            List<object> list = new List<object> { "p", "q", "r" };
            adapter.AddAll(list, 11);
            Assert.Equal(3, adapter.GetItemCount());
            Assert.Equal(11, adapter.GetItemViewType(2));
            adapter.Set(new List<object> { "v", "w", "z" }, 11);
            Assert.Equal(3, adapter.GetItemCount());
            Assert.Equal(11, adapter.GetItemViewType(0));
        }

        [Fact]
        public void TestRemoveClearPublic()
        {
            var adapter = new MultiTypeAdapter(context);
            adapter.AddViewTypeToLayoutMap(7, 107);
            adapter.Add("car", 7);
            Assert.Equal(1, adapter.GetItemCount());
            adapter.Remove(0);
            Assert.Equal(0, adapter.GetItemCount());
            adapter.Add("bus", 7);
            adapter.Clear();
            Assert.Equal(0, adapter.GetItemCount());
        }

        [Fact]
        public void TestSetWithTyperPublic()
        {
            var typerMock = new Mock<MultiTypeAdapter.MultiViewTyper>();
            typerMock.Setup(t => t.GetViewType(It.IsAny<object>())).Returns(4);
            var adapter = new MultiTypeAdapter(context);
            adapter.AddViewTypeToLayoutMap(4, 104);
            adapter.Set(new List<object> { "k", "l", "m" }, typerMock.Object);
            Assert.Equal(3, adapter.GetItemCount());
            Assert.Equal(4, adapter.GetItemViewType(2));
        }

        [Fact]
        public void TestAddAtPositionAndAddAllPositionPublic()
        {
            var adapter = new MultiTypeAdapter(context);
            adapter.AddViewTypeToLayoutMap(15, 115);
            adapter.Add("apple", 15);
            adapter.Add(0, "banana", 15);
            List<object> list = new List<object> { "pear", "peach" };
            adapter.AddAll(0, list, 15);
            Assert.Equal(4, adapter.GetItemCount());
            Assert.Equal(15, adapter.GetItemViewType(3));
        }
    }
}