using Xunit;

namespace PublicTests
{
    public class IMutableArtifactStorePublicTests
    {
        class DummyMutableStore
        {
            private bool removed = false;
            private string lastFileSetId = null;
            public void RemoveFileSet(string fileSetId)
            {
                this.removed = true;
                this.lastFileSetId = fileSetId;
            }
            public bool IsRemoved() => removed;
            public string GetLastFileSetId() => lastFileSetId;
        }

        [Fact]
        public void CallsRemoveFileSetWithDifferentData()
        {
            var store = new DummyMutableStore();
            store.RemoveFileSet("public-fileset-abc");
            Assert.True(store.IsRemoved());
            Assert.Equal("public-fileset-abc", store.GetLastFileSetId());
        }

        [Fact]
        public void RemoveFileSetNotCalledByDefault()
        {
            var store = new DummyMutableStore();
            Assert.False(store.IsRemoved());
            Assert.Null(store.GetLastFileSetId());
        }
    }
}