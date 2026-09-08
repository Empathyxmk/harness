using System.Collections.Generic;
using Xunit;
using Moq;
using MarkZhai.DataBindingAdapter;

namespace MarkZhai.DataBindingAdapter.Tests.Original
{
    public class SingleTypeAdapterTest
    {
        private object context;
        private object inflater;

        public SingleTypeAdapterTest()
        {
            context = new object();
            inflater = new object();
        }

        [Fact]
        public void TestConstructorAndGetters()
        {
            var adapter = new SingleTypeAdapter<string>(context, 123);
            Assert.Equal(0, adapter.GetItemCount());
            Assert.Equal(123, adapter.GetLayoutRes());
        }

        [Fact]
        public void TestAdd()
        {
            var adapter = new SingleTypeAdapter<string>(context, 321);
            adapter.Add("foo");
            Assert.Equal(1, adapter.GetItemCount());
        }

        [Fact]
        public void TestAddAtPosition()
        {
            var adapter = new SingleTypeAdapter<string>(context, 321);
            adapter.Add("foo");
            adapter.Add(0, "bar");
            Assert.Equal(2, adapter.GetItemCount());
        }

        [Fact]
        public void TestSetAndAddAll()
        {
            var adapter = new SingleTypeAdapter<string>(context, 321);
            adapter.Set(new List<string> { "a", "b" });
            Assert.Equal(2, adapter.GetItemCount());
            adapter.AddAll(new List<string> { "c" });
            Assert.Equal(3, adapter.GetItemCount());
        }
    }
}