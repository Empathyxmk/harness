using System.IO.Compression;
using Xunit;

namespace Casidiablo.MultiDex.Tests.Public
{
    public class ZipUtilExtraPublicTest
    {
        [Fact]
        public void TestZipEntryNoExtraDataPublic()
        {
            var entry = new ZipArchiveEntryFake("anotherfile.txt");
            Assert.Null(entry.Extra);
            entry.Extra = new byte[0];
            Assert.NotNull(entry.Extra);
            Assert.Equal(0, entry.Extra.Length);
        }

        [Fact]
        public void TestZipEntryWithExtraDataPublic()
        {
            var entry = new ZipArchiveEntryFake("some_entry.txt");
            var extra = new byte[] { 42, 7, 100, 5 };
            entry.Extra = extra;
            Assert.Equal(extra, entry.Extra);
        }

        private class ZipArchiveEntryFake
        {
            public string Name { get; }
            public byte[] Extra { get; set; }
            public ZipArchiveEntryFake(string name) { Name = name; }
        }
    }
}