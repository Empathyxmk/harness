using System;
using System.Collections.Generic;
using System.IO;
using Xunit;

namespace Casidiablo.MultiDex.Tests.Original
{
    public class MultiDexExtractorTest : IDisposable
    {
        private FileInfo tempApk;

        public MultiDexExtractorTest()
        {
            // Create a temp file pretending to be APK
            tempApk = new FileInfo(Path.GetTempFileName() + ".apk");
            using (var fs = new FileStream(tempApk.FullName, FileMode.Create))
            using (var zos = new System.IO.Compression.ZipArchive(fs, System.IO.Compression.ZipArchiveMode.Create, leaveOpen: true))
            {
                var entry = zos.CreateEntry("classes.dex");
                using (var entryStream = entry.Open())
                {
                    var data = System.Text.Encoding.UTF8.GetBytes("01234567");
                    entryStream.Write(data, 0, data.Length);
                }
            }
            tempApk.Refresh();
        }

        [Fact]
        public void TestLoadWithNoSecondaryDex()
        {
            var info = new MockApplicationInfo(tempApk.FullName);
            var dexDir = new DirectoryInfo(Path.GetTempPath());
            var files = MultiDexExtractor.Load(null, info, dexDir, false);
            Assert.NotNull(files);
        }

        [Fact]
        public void TestBadZipCrcFileThrows()
        {
            var fake = new FileInfo(Path.GetTempFileName() + ".apk");
            using (var sw = new StreamWriter(fake.OpenWrite()))
            {
                sw.Write("notazip");
            }
            var info = new MockApplicationInfo(fake.FullName);
            var ex = Assert.Throws<IOException>(() => MultiDexExtractor.Load(null, info, fake.Directory, false));
            fake.Delete();
        }

        public void Dispose()
        {
            if (tempApk.Exists)
                tempApk.Delete();
        }

        class MockApplicationInfo
        {
            public string SourceDir { get; }
            public MockApplicationInfo(string sourceDir)
            {
                SourceDir = sourceDir;
            }
        }
    }
}