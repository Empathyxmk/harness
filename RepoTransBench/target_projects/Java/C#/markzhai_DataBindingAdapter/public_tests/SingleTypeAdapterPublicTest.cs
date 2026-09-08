using System.Collections.Generic;
using Xunit;
using MarkZhai.DataBindingAdapter;

namespace MarkZhai.DataBindingAdapter.Tests.Public
{
    public class SingleTypeAdapterPublicTest
    {
        private object context;
        private object inflater;

        public SingleTypeAdapterPublicTest()
        {
            context = new object();
            inflater = new object();
        }

        [Fact]
        public void TestAddAndCountPublic()
        {
            var adapter = new SingleTypeAdapter<string>(context, 1222);
            adapter.Add("delta");
            Assert.Equal(1, adapter.GetItemCount());
            Assert.Equal(1222, adapter.GetLayoutRes());
        }

        [Fact]
        public void TestAddAtPositionPublic()
        {
            var adapter = new SingleTypeAdapter<string>(context, 2121);
            adapter.Add("sigma");
            adapter.Add(0, "theta");
            Assert.Equal(2, adapter.GetItemCount());
            Assert.Equal("theta", adapter.mCollection[0]);
            Assert.Equal("sigma", adapter.mCollection[1]);
        }

        [Fact]
        public void TestSetPublic()
        {
            var adapter = new SingleTypeAdapter<string>(context, 3333);
            var items = new List<string> { "alpha", "beta", "gamma" };
            adapter.Set(items);
            Assert.Equal(3, adapter.GetItemCount());
            Assert.Equal("alpha", adapter.mCollection[0]);
            Assert.Equal("gamma", adapter.mCollection[2]);
        }

        [Fact]
        public void TestAddAllPublic()
        {
            var adapter = new SingleTypeAdapter<string>(context, 4343);
            var items = new List<string> { "one", "two" };
            adapter.AddAll(items);
            Assert.Equal(2, adapter.GetItemCount());
            adapter.Add("three");
            Assert.Equal(3, adapter.GetItemCount());
        }
    }
}