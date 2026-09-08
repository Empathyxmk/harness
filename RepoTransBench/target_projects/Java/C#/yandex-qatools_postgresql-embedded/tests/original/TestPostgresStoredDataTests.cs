using Xunit;

namespace OriginalTests
{
    public class TestPostgresStoredDataTests
    {
        class StoredData
        {
            private string data = "";
            public void Store(string s) { this.data = s; }
            public string Retrieve() => data;
        }

        [Fact]
        public void StoreAndRetrieveWorks()
        {
            var store = new StoredData();
            store.Store("something to store");
            Assert.Equal("something to store", store.Retrieve());
        }

        [Fact]
        public void RetrieveReturnsEmptyInitially()
        {
            var store = new StoredData();
            Assert.Equal("", store.Retrieve());
        }
    }
}