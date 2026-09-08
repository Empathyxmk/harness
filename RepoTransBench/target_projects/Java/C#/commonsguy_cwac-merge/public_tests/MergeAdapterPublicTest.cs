using System;
using System.Collections.Generic;
using Xunit;
using CommonsGuy.Cwac.Merge;

namespace CommonsGuy.Cwac.Merge.PublicTests
{
    public class MergeAdapterPublicTest
    {
        [Fact]
        public void TestSingleAdapterDifferentData()
        {
            // Use different data from existing test!
            var dummy = new DummyAdapter(new List<int> {42, 7, 18});
            var merge = new MergeAdapter(dummy);

            Assert.Equal(3, merge.GetCount());
            Assert.Equal(42, merge.GetItem(0));
            Assert.Equal(7, merge.GetItem(1));
            Assert.Equal(18, merge.GetItem(2));
        }

        [Fact]
        public void TestMultipleAdaptersDifferentData()
        {
            var dummyA = new DummyAdapter(new List<int> {91, 22});
            var dummyB = new DummyAdapter(new List<int> {55, 66});
            var merge = new MergeAdapter();
            merge.AddAdapter(dummyA);
            merge.AddAdapter(dummyB);

            Assert.Equal(4, merge.GetCount());
            Assert.Equal(91, merge.GetItem(0));
            Assert.Equal(22, merge.GetItem(1));
            Assert.Equal(55, merge.GetItem(2));
            Assert.Equal(66, merge.GetItem(3));
        }
    }
}