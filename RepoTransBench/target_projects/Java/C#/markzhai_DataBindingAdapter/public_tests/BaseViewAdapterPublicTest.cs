using System.Collections.Generic;
using Xunit;
using MarkZhai.DataBindingAdapter;

namespace MarkZhai.DataBindingAdapter.Tests.Public
{
    public class BaseViewAdapterPublicTest
    {
        private object context;
        private object inflater;

        private class TestAdapter : BaseViewAdapter<string>
        {
            public TestAdapter(object context)
            { }
            public override BindingViewHolder<object> OnCreateViewHolder(object parent, int viewType) => null;
            public override void OnBindViewHolder(BindingViewHolder<object> holder, int position) { }
        }

        public BaseViewAdapterPublicTest()
        {
            context = new object();
            inflater = new object();
        }

        [Fact]
        public void TestAddSetClearPublic()
        {
            var adapter = new TestAdapter(context);
            adapter.Add("red");
            Assert.Equal(1, adapter.GetItemCount());
            adapter.Set(new List<string> { "yellow", "green", "blue" });
            Assert.Equal(3, adapter.GetItemCount());
            adapter.Clear();
            Assert.Equal(0, adapter.GetItemCount());
        }

        [Fact]
        public void TestRemoveGetPublic()
        {
            var adapter = new TestAdapter(context);
            adapter.Set(new List<string> { "x", "y", "z" });
            Assert.Equal("y", adapter.Get(1));
            adapter.Remove(0);
            Assert.Equal("y", adapter.Get(0));
            Assert.Equal(2, adapter.GetItemCount());
        }
    }
}