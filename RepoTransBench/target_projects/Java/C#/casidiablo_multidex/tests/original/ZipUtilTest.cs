using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using System.Linq;
using Xunit;

namespace Casidiablo.MultiDex.Tests.Original
{
    public class ZipUtilTest
    {
        private static readonly FileInfo _zipFile = new FileInfo(
            Path.Combine(Environment.GetEnvironmentVariable("ANDROID_BUILD_TOP") ?? ".", "out/target/common/obj/JAVA_LIBRARIES/android-support-multidex_intermediates/javalib.jar")
        );

        [Fact]
        public void SetupClass_ValidZip()
        {
            using var zip = ZipFile.OpenRead(_zipFile.FullName);
            // No exception means OK
        }

        [Fact]
        public void TestCrcDoNotCrash()
        {
            long crc = ZipUtil.GetZipCrc(_zipFile.FullName);
            Console.WriteLine("crc is " + crc);
        }

        [Fact]
        public void TestCrcRange()
        {
            var zipEntries = new Dictionary<string, ZipArchiveEntry>();
            using var zip = ZipFile.OpenRead(_zipFile.FullName);
            foreach (var entry in zip.Entries)
                zipEntries[entry.FullName] = entry;

            var checkedEntries = ZipEntryReader.ReadAllEntries(_zipFile.FullName);

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
        public void TestCrcValue()
        {
            using var zip = ZipFile.OpenRead(_zipFile.FullName);
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
        public void TestInvalidCrcValue()
        {
            using var zip = ZipFile.OpenRead(_zipFile.FullName);
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
                        Size = new FileInfo(tempPath).Length - 1
                    };
                    long crc = ZipUtil.ComputeCrcOfCentralDir(tempPath, dir);
                    Assert.NotEqual(refEntry.Crc32, crc);
                    File.Delete(tempPath);
                }
            }
        }
    }
}