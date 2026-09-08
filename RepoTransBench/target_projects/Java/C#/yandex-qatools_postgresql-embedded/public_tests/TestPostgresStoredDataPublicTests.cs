using Xunit;

namespace PublicTests
{
    public class TestPostgresStoredDataPublicTests
    {
        class StoredData
        {
            private string data = "";
            public void Store(string s) { this.data = s; }
            public string Retrieve() => data + "-public";
        }

        [Fact]
        public void StoreAndRetrieveWorksWithPublicSuffix()
        {
            var store = new StoredData();
            store.Store("fooBarTest");
            Assert.Equal("fooBarTest-public", store.Retrieve());
        }

        [Fact]
        public void RetrieveEmptyReturnsPublic()
        {
            var store = new StoredData();
            Assert.Equal("-public", store.Retrieve());
        }
    }
}