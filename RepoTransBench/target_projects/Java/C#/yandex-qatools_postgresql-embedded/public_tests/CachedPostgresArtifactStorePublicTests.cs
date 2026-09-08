using Xunit;

namespace PublicTests
{
    public class CachedPostgresArtifactStorePublicTests
    {
        class DummyCache
        {
            private string fileName;
            private int timesFetched = 0;
            public DummyCache(string fileName) { this.fileName = fileName; }
            public string Fetch() { timesFetched++; return "fetched_public_" + fileName; }
            public int GetTimesFetched() => timesFetched;
        }

        [Fact]
        public void FetchReturnsFileWithDifferentName()
        {
            var cache = new DummyCache("pubfile-2211.txt");
            var res = cache.Fetch();
            Assert.Contains("pubfile-2211.txt", res);
        }

        [Fact]
        public void FetchCountsTimesFetchedWithDifferentFile()
        {
            var cache = new DummyCache("pubcache.data");
            cache.Fetch();
            cache.Fetch();
            Assert.Equal(2, cache.GetTimesFetched());
        }
    }
}