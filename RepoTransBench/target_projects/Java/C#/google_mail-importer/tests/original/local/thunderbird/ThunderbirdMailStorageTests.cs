using System.IO;
using Xunit;

namespace GoogleMailImporter.Tests.Original.Local.Thunderbird
{
    public class ThunderbirdMailStorageTests
    {
        [Fact]
        public void CreateFromFile()
        {
            var file = new FileInfo("/tmp/mailbox");
            var storage = new ThunderbirdMailStorage(file);
            Assert.NotNull(storage);
        }
    }

    public class ThunderbirdMailStorage
    {
        public ThunderbirdMailStorage(FileInfo file)
        {
            // Just store for test
        }
    }
}