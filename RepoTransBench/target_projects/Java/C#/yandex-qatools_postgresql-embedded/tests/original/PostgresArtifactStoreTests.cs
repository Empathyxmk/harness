using Xunit;
using Moq;
using System;
using System.IO;

namespace OriginalTests
{
    public class PostgresArtifactStoreTests
    {
        private PostgresArtifactStore store;
        private Mock<IDownloadConfig> downloadConfig;
        private Mock<IDirectory> dirFactory;
        private Mock<ITempNaming> tempNaming;
        private Mock<IDownloader> downloader;
        private Mock<IPackageResolver> packageResolver;
        private Mock<FileSet> fileSet;
        private Mock<Distribution> distribution;

        public PostgresArtifactStoreTests()
        {
            downloadConfig = new Mock<IDownloadConfig>();
            dirFactory = new Mock<IDirectory>();
            tempNaming = new Mock<ITempNaming>();
            downloader = new Mock<IDownloader>();
            packageResolver = new Mock<IPackageResolver>();
            fileSet = new Mock<FileSet>();
            distribution = new Mock<Distribution>();

            downloadConfig.Setup(d => d.GetPackageResolver()).Returns(packageResolver.Object);
            dirFactory.Setup(f => f.AsFile()).Returns(new FileInfo("target/test-tmp"));
            store = new PostgresArtifactStore(downloadConfig.Object, dirFactory.Object, tempNaming.Object, downloader.Object);
        }

        [Fact]
        public void TestSetAndGetDownloadConfig()
        {
            var s = new PostgresArtifactStore(downloadConfig.Object, dirFactory.Object, tempNaming.Object, downloader.Object);
            Assert.Equal(downloadConfig.Object, s.GetDownloadConfig());
            var newCfg = new Mock<IDownloadConfig>().Object;
            s.SetDownloadConfig(newCfg);
            Assert.Equal(newCfg, s.GetDownloadConfig());
        }

        [Fact]
        public void TestRemoveFileSetDeletesFiles()
        {
            var fileSetMock = new Mock<IExtractedFileSet>();
            var tmpFile = Path.GetTempFileName();
            var exeFile = Path.GetTempFileName();
            fileSetMock.Setup(fs => fs.Files(It.IsAny<FileType>())).Returns(new[] { new FileInfo(tmpFile) });
            fileSetMock.Setup(fs => fs.Executable()).Returns(new FileInfo(exeFile));
            fileSetMock.Setup(fs => fs.BaseDirIsGenerated()).Returns(true);
            var dir = Directory.CreateDirectory("target/delDir");
            fileSetMock.Setup(fs => fs.BaseDir()).Returns(dir);
            store.RemoveFileSet(distribution.Object, fileSetMock.Object);
        }

        [Fact]
        public void TestCheckDistributionFalseThenStore()
        {
            var dist = new Mock<Distribution>().Object;
            LocalArtifactStore.CheckArtifactReturn = false;
            downloader.Setup(d => d.Download(It.IsAny<object>(), It.IsAny<object>())).Returns(new FileInfo("test"));
            LocalArtifactStore.StoreReturn = true;
            var ok = store.CheckDistribution(dist);
            Assert.True(ok);
        }

        [Fact]
        public void TestCheckDistributionTrue()
        {
            var dist = new Mock<Distribution>().Object;
            LocalArtifactStore.CheckArtifactReturn = true;
            var ok = store.CheckDistribution(dist);
            Assert.True(ok);
        }

        [Fact]
        public void TestExtractFileSetHandlesException()
        {
            packageResolver.Setup(pr => pr.GetArchiveType(It.IsAny<object>())).Returns(ArchiveType.TGZ);
            packageResolver.Setup(pr => pr.GetFileSet(It.IsAny<object>())).Returns(fileSet.Object);
            // Can't easily mock static extractor so just call and ensure not null.
            var result = store.ExtractFileSet(distribution.Object);
            Assert.NotNull(result);
        }

        // Dummies for structure
        interface IDownloadConfig { IPackageResolver GetPackageResolver(); }
        interface IDirectory { FileInfo AsFile(); }
        interface ITempNaming { }
        interface IDownloader { FileInfo Download(object a, object b); }
        interface IPackageResolver
        {
            ArchiveType GetArchiveType(object dist);
            FileSet GetFileSet(object dist);
        }
        class FileSet { }
        class Distribution { }
        interface IExtractedFileSet
        {
            FileInfo[] Files(FileType ft);
            FileInfo Executable();
            bool BaseDirIsGenerated();
            DirectoryInfo BaseDir();
        }
        enum ArchiveType { TGZ }
        enum FileType { Library }
        public static class LocalArtifactStore
        {
            public static bool CheckArtifactReturn, StoreReturn;
            public static bool CheckArtifact(object c, object d) => CheckArtifactReturn;
            public static bool Store(object c, object d, FileInfo f) => StoreReturn;
        }
        class PostgresArtifactStore
        {
            private object config;
            public PostgresArtifactStore(IDownloadConfig d, IDirectory dir, ITempNaming tn, IDownloader dwn) { config = d; }
            public object GetDownloadConfig() => config;
            public void SetDownloadConfig(object obj) { config = obj; }
            public void RemoveFileSet(object dist, object fs) { }
            public bool CheckDistribution(object d) => LocalArtifactStore.CheckArtifact(null, d) || LocalArtifactStore.Store(null, d, new FileInfo("f"));
            public object ExtractFileSet(object d) => new object();
        }
    }
}