using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using Xunit;

namespace Casidiablo.MultiDex.Tests.Public
{
    public class ZipUtilPublicTest
    {
        private static readonly FileInfo zipFile = CreatePublicTestZip();

        private static FileInfo CreatePublicTestZip()
        {
            string path = Path.GetTempFileName() + ".zip";
            using (var fs = new FileStream(path, FileMode.Create))
            using (var zs = new ZipArchive(fs, ZipArchiveMode.Create))
            {
                var entry1 = zs.CreateEntry("file1.txt");
                using (var entry1Stream = entry1.Open()) {
                    var data = System.Text.Encoding.UTF8.GetBytes("hello");
                    entry1Stream.Write(data, 0, data.Length);
                }
                var entry2 = zs.CreateEntry("file2.txt");
                using (var entry2Stream = entry2.Open()) {
                    var data = System.Text.Encoding.UTF8.GetBytes("world");
                    entry2Stream.Write(data, 0, data.Length);
                }
            }
            return new FileInfo(path);
        }

        [Fact]
        public void TestCrcDoNotCrashPublic()
        {
            long crc = ZipUtil.GetZipCrc(zipFile.FullName);
            Assert.True(crc > 0);
        }

        [Fact]
        public void TestCrcRangePublic()
        {
            var zipEntries = new Dictionary<string, ZipArchiveEntry>();
            using (var zip = ZipFile.OpenRead(zipFile.FullName))
            {
                foreach (var entry in zip.Entries)
                    zipEntries[entry.FullName] = entry;
            }

            var checkedEntries = ZipEntryReader.ReadAllEntries(zipFile.FullName);

            Assert.Equal(zipEntries.Count, checkedEntries.Count);
            foreach (var refEntry in zipEntries.Values)
            {
                Assert.True(checkedEntries.ContainsKey(refEntry.FullName));
                var checkEntry = checkedEntries[refEntry.FullName];
                Assert.Equal(refEntry.FullName, checkEntry.FullName);
                Assert.Equal(refEntry.Comment, checkEntry.Comment);
                Assert.Equal(refEntry.LastWriteTime, checkEntry.LastWriteTime);
                Assert.Equal(refEntry.Crc32, checkEntry.Crc32);
                Assert.Equal(refEntry.CompressedLength, checkEntry.CompressedLength);
                Assert.Equal(refEntry.Length, checkEntry.Length);
                Assert.Equal(refEntry.CompressionMethod, checkEntry.CompressionMethod);
                Assert.Equal(refEntry.Extra, checkEntry.Extra);
            }
        }

        [Fact]
        public void TestCrcValuePublic()
        {
            using var zip = ZipFile.OpenRead(zipFile.FullName);
            byte[] buffer = new byte[0x2000];
            foreach (var refEntry in zip.Entries)
            {
                if (refEntry.Length > 0)
                {
                    string tempPath = Path.GetTempFileName();
                    using (var inStream = refEntry.Open())
                    using (var outStream = new FileStream(tempPath, FileMode.Create, FileAccess.Write))
                    {
                        int read;
                        while ((read = inStream.Read(buffer, 0, buffer.Length)) > 0)
                        {
                            outStream.Write(buffer, 0, read);
                        }
                    }
                    var dir = new CentralDirectory()
                    {
                        Offset = 0,
                        Size = new FileInfo(tempPath).Length
                    };
                    long crc = ZipUtil.ComputeCrcOfCentralDir(tempPath, dir);
                    Assert.Equal(refEntry.Crc32, crc);
                    File.Delete(tempPath);
                }
            }
        }

        [Fact]
        public void TestInvalidCrcValuePublic()
        {
            using var zip = ZipFile.OpenRead(zipFile.FullName);
            byte[] buffer = new byte[0x2000];
            foreach (var refEntry in zip.Entries)
            {
                if (refEntry.Length > 0)
                {
                    string tempPath = Path.GetTempFileName();
                    using (var inStream = refEntry.Open())
                    using (var outStream = new FileStream(tempPath, FileMode.Create, FileAccess.Write))
                    {
                        int read;
                        while ((read = inStream.Read(buffer, 0, buffer.Length)) > 0)
                        {
                            outStream.Write(buffer, 0, read);
                        }
                    }
                    var dir = new CentralDirectory()
                    {
                        Offset = 0,
                        Size = new FileInfo(tempPath).Length - 2
                    };
                    long crc = ZipUtil.ComputeCrcOfCentralDir(tempPath, dir);
                    Assert.NotEqual(refEntry.Crc32, crc);
                    File.Delete(tempPath);
                }
            }
        }
    }
}