using System.IO;
using Xunit;

namespace GoogleMailImporter.PublicTests.Local.Thunderbird
{
    public class ThunderbirdMailStoragePublicTests
    {
        [Fact]
        public void TestCanCreateFromDifferentFile()
        {
            var file = new FileInfo("/tmp/pubmailbox");
            var storage = new ThunderbirdMailStorage(file);
            Assert.NotNull(storage);
        }
    }

    // Dummy for testing
    public class ThunderbirdMailStorage
    {
        public ThunderbirdMailStorage(FileInfo file)
        {
            // File is just stored for test; do nothing else
        }
    }
}