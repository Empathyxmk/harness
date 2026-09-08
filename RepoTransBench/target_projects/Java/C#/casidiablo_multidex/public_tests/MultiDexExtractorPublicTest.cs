using System;
using System.IO;
using Xunit;

namespace Casidiablo.MultiDex.Tests.Public
{
    public class MultiDexExtractorPublicTest
    {
        [Fact]
        public void TestNonExistentFileCannotFindCentralDirectoryPublic()
        {
            var fake = new FileInfo("this_file_should_not_exist_" + DateTime.Now.Ticks + ".zip");
            try
            {
                using (var fs = new FileStream(fake.FullName, FileMode.Open))
                {
                    ZipUtil.FindCentralDirectory(fs);
                    Assert.True(false, "Should have thrown because file doesn't exist");
                }
            }
            catch
            {
                // expected
            }
        }

        [Fact]
        public void TestGetZipCrcNonExistentFilePublic()
        {
            try
            {
                long crc = ZipUtil.GetZipCrc("definitely_not_here_" + DateTime.Now.Ticks + ".zip");
                Assert.True(false, "Should not succeed on non-existent");
            }
            catch
            {
                // expected
            }
        }
    }
}