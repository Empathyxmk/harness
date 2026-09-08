using Xunit;
using PocketSphinx;
using System;

namespace PocketSphinxTests.Public
{
    public class AssetsPublicTests
    {
        [Fact]
        public void TestAssetsConstructorWithDifferentDest()
        {
            var assets = new Assets(null, "public_dest_dir_v2");
            Assert.NotNull(assets);
        }

        [Fact]
        public void TestSyncMethodThrowsExceptionWithPublicData()
        {
            var assets = new Assets(null, "public_dest_dir_v2");
            Assert.Throws<Exception>(() => assets.Sync());
        }
    }
}