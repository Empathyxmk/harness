using System;
using Xunit;

namespace GridListViewAdapters.Tests
{
    public class BaseGridAdapterTests
    {
        private class DummyGridAdapter : BaseGridAdapter
        {
            public DummyGridAdapter() : base(null, 1, 1) { }
        }

        private DummyGridAdapter adapter;

        public BaseGridAdapterTests()
        {
            adapter = new DummyGridAdapter();
        }

        [Fact]
        public void GetCount_DoesNotThrow()
        {
            adapter.GetCount();
        }

        [Fact]
        public void GetNumOfColumns_DoesNotThrow()
        {
            adapter.GetNumOfColumns();
        }

        [Fact]
        public void GetNumOfRows_DoesNotThrow()
        {
            adapter.GetNumOfRows();
        }
    }
}