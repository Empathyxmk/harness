using Xunit;

namespace GridListViewAdapters.PublicTests
{
    public class CursorGridAdapterPublicTests
    {
        private class DummyCursorGridAdapter : CursorGridAdapter
        {
            public DummyCursorGridAdapter() : base(null, 4, 2) { }
        }

        [Fact]
        public void InstantiationPublic_DoesNotThrow()
        {
            var adapter = new DummyCursorGridAdapter();
            adapter.GetCount();
            adapter.GetNumOfRows();
            adapter.GetNumOfColumns();
        }
    }
}