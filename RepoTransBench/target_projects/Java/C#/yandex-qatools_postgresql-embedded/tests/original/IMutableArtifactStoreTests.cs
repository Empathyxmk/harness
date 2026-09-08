using Xunit;

namespace OriginalTests
{
    public class IMutableArtifactStoreTests
    {
        class TestMutableArtifactStore : IMutableArtifactStore
        {
            public bool ConfigSet = false;
            public void SetDownloadConfig(object c) { ConfigSet = true; }
            public void RemoveFileSet(object d, object fs) { }
            public bool CheckDistribution(object d) => false;
            public object ExtractFileSet(object d) => null;
        }

        interface IMutableArtifactStore
        {
            void SetDownloadConfig(object c);
            void RemoveFileSet(object d, object f);
            bool CheckDistribution(object d);
            object ExtractFileSet(object d);
        }

        [Fact]
        public void TestSetDownloadConfig()
        {
            var store = new TestMutableArtifactStore();
            Assert.False(store.ConfigSet);
            store.SetDownloadConfig(null);
            Assert.True(store.ConfigSet);
        }
    }
}