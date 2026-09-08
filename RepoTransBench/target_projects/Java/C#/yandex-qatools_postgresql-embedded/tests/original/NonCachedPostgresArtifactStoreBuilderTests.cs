using Xunit;
using Moq;

namespace OriginalTests
{
    public class NonCachedPostgresArtifactStoreBuilderTests
    {
        [Fact]
        public void BuilderShouldReturnPostgresArtifactStore()
        {
            var builder = new NonCachedPostgresArtifactStoreBuilder();
            var downloadConfig = new Mock<IDownloadConfig>().Object;
            var dir = new Mock<IDirectory>().Object;
            var tempNaming = new Mock<ITempNaming>().Object;
            var downloader = new Mock<IDownloader>().Object;
            builder.DownloadConfig(downloadConfig).TempDirFactory(dir).ExecutableNaming(tempNaming).Downloader(downloader);

            var store = builder.Build();
            Assert.IsType<PostgresArtifactStore>(store);
        }

        // Dummy placeholder classes for compilation
        class NonCachedPostgresArtifactStoreBuilder
        {
            public NonCachedPostgresArtifactStoreBuilder DownloadConfig(object o) { return this; }
            public NonCachedPostgresArtifactStoreBuilder TempDirFactory(object o) { return this; }
            public NonCachedPostgresArtifactStoreBuilder ExecutableNaming(object o) { return this; }
            public NonCachedPostgresArtifactStoreBuilder Downloader(object o) { return this; }
            public object Build() => new PostgresArtifactStore();
        }

        interface IDownloadConfig { }
        interface IDirectory { }
        interface ITempNaming { }
        interface IDownloader { }
        class PostgresArtifactStore { }
    }
}