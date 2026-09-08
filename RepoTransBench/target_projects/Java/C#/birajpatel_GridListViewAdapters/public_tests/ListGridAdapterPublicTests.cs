using Xunit;

namespace GridListViewAdapters.PublicTests
{
    public class ListGridAdapterPublicTests
    {
        private class DummyListGridAdapter : ListGridAdapter
        {
            public DummyListGridAdapter() : base(null, 2, 3) { }
        }

        [Fact]
        public void Instantiation_DoesNotThrow()
        {
            var adapter = new DummyListGridAdapter();
            adapter.GetCount();
            adapter.GetNumOfRows();
            adapter.GetNumOfColumns();
        }
    }
}