using System;
using System.Collections.Generic;
using Xunit;
using CommonsGuy.Cwac.Merge;

namespace CommonsGuy.Cwac.Merge.Tests
{
    public class MergeAdapterTest
    {
        [Fact]
        public void TestSingleAdapter()
        {
            var dummy = new DummyAdapter(new List<int> {1, 2, 3});
            var merge = new MergeAdapter(dummy);

            Assert.Equal(3, merge.GetCount());
            Assert.Equal(1, merge.GetItem(0));
            Assert.Equal(2, merge.GetItem(1));
            Assert.Equal(3, merge.GetItem(2));
        }

        [Fact]
        public void TestMultipleAdapters()
        {
            var dummy = new DummyAdapter(new List<int> {10, 20});
            var dummy2 = new DummyAdapter(new List<int> {30});
            var merge = new MergeAdapter();
            merge.AddAdapter(dummy);
            merge.AddAdapter(dummy2);

            Assert.Equal(3, merge.GetCount());
            Assert.Equal(10, merge.GetItem(0));
            Assert.Equal(20, merge.GetItem(1));
            Assert.Equal(30, merge.GetItem(2));
        }
    }
}