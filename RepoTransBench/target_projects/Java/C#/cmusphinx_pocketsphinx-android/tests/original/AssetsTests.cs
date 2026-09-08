using Xunit;
using PocketSphinx;
using System;

namespace PocketSphinxTests.Original
{
    public class AssetsTests
    {
        [Fact]
        public void TestAssetsConstructorWithDest()
        {
            var assets = new Assets(null, "test_dest_dir");
            Assert.NotNull(assets);
        }

        [Fact]
        public void TestSyncMethodThrowsException()
        {
            var assets = new Assets(null, "test_dest_dir");
            Assert.Throws<Exception>(() => assets.Sync());
        }
    }
}