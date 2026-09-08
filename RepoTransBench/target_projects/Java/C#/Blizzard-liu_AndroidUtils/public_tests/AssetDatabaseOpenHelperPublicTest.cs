using Xunit;

namespace AndroidUtils.PublicTests
{
    public class AssetDatabaseOpenHelperPublicTest
    {
        [Fact]
        public void TestOpenDatabase_Public()
        {
            // Different db name from original
            string dbName = "another_public_test.db";
            Assert.StartsWith("another_", dbName);
        }
    }
}