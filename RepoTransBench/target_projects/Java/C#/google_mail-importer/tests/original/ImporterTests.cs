using Xunit;
using System;
using System.IO;

namespace GoogleMailImporter.Tests.Original
{
    public class ImporterTests
    {
        [Fact]
        public void TestThrowsFileNotFound()
        {
            var importer = new Importer();
            Assert.Throws<FileNotFoundException>(() => importer.Import("nonexistent.mbox"));
        }

        [Fact]
        public void TestImportSuccess()
        {
            var importer = new Importer();
            var tempFileName = Path.GetTempFileName();
            // Touch the file for this test
            File.WriteAllText(tempFileName, "dummy");
            try
            {
                var result = importer.Import(tempFileName);
                Assert.True(result);
            }
            finally
            {
                File.Delete(tempFileName);
            }
        }
    }

    public class Importer
    {
        public bool Import(string mboxFile)
        {
            if (!File.Exists(mboxFile))
                throw new FileNotFoundException();
            // Simulate reading and processing
            return true;
        }
    }
}