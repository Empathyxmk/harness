using Xunit;

namespace GridListViewAdapters.PublicTests
{
    public class BaseGridAdapterPublicTests
    {
        private class DummyGridAdapter : BaseGridAdapter
        {
            public DummyGridAdapter() : base(null, 3, 4) // public test: 3 columns, 4 rows
            {
            }
        }

        private DummyGridAdapter adapter;

        public BaseGridAdapterPublicTests()
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