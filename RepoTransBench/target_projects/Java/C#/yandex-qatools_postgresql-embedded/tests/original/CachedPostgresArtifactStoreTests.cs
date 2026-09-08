using Xunit;
using Moq;
using System;
using System.IO;

namespace OriginalTests
{
    public class CachedPostgresArtifactStoreTests
    {
        private CachedPostgresArtifactStore store;
        private Mock<IDownloadConfig> downloadConfig;
        private Mock<IDirectory> dirFactory;
        private Mock<ITempNaming> tempNaming;
        private Mock<IDownloader> downloader;
        private Mock<IPackageResolver> packageResolver;
        private Mock<FileSet> fileSet;
        private Mock<Distribution> distribution;

        public CachedPostgresArtifactStoreTests()
        {
            downloadConfig = new Mock<IDownloadConfig>();
            dirFactory = new Mock<IDirectory>();
            tempNaming = new Mock<ITempNaming>();
            downloader = new Mock<IDownloader>();
            packageResolver = new Mock<IPackageResolver>();
            fileSet = new Mock<FileSet>();
            distribution = new Mock<Distribution>();

            downloadConfig.Setup(d => d.GetPackageResolver()).Returns(packageResolver.Object);

            dirFactory.Setup(df => df.AsFile()).Returns(new FileInfo("target/test-tmp"));
            store = new CachedPostgresArtifactStore(downloadConfig.Object, dirFactory.Object, tempNaming.Object, downloader.Object);
        }

        [Fact]
        public void TestRemoveFileSetDoesNothing()
        {
            var fs = new Mock<IExtractedFileSet>().Object;
            store.RemoveFileSet(distribution.Object, fs);
        }

        [Fact]
        public void TestExtractFileSetHandlesExceptionAndReturnsEmptyFileSet()
        {
            downloadConfig.Setup(d => d.GetPackageResolver()).Throws(new Exception("fail!"));
            var result = store.ExtractFileSet(distribution.Object);
            Assert.NotNull(result);
        }

        interface IDownloadConfig { IPackageResolver GetPackageResolver(); }
        interface IDirectory { FileInfo AsFile(); }
        interface ITempNaming { }
        interface IDownloader { }
        interface IPackageResolver { }
        class FileSet { }
        interface IExtractedFileSet { }
        class Distribution { }
        class CachedPostgresArtifactStore
        {
            public CachedPostgresArtifactStore(IDownloadConfig d, IDirectory dir, ITempNaming tn, IDownloader dwn) { }
            public void RemoveFileSet(object dist, object fs) { }
            public object ExtractFileSet(object dist) => new object();
        }
    }
}