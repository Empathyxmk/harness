using Xunit;

namespace PublicTests
{
    public class PostgresArtifactStorePublicTests
    {
        class PostgresArtifactStoreFake
        {
            private string artifact;
            public PostgresArtifactStoreFake(string artifact) { this.artifact = artifact; }
            public string GetArtifact() => artifact;
            public void SetArtifact(string artifact) { this.artifact = artifact; }
        }

        [Fact]
        public void StoresArtifactNameWithDifferentValue()
        {
            var store = new PostgresArtifactStoreFake("public-art-unique-192");
            Assert.Equal("public-art-unique-192", store.GetArtifact());
        }

        [Fact]
        public void SetArtifactUpdatesArtifactWithAnotherValue()
        {
            var store = new PostgresArtifactStoreFake("start-art-public-1");
            store.SetArtifact("set-artifact-public-2");
            Assert.Equal("set-artifact-public-2", store.GetArtifact());
        }
    }
}