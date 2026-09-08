using Xunit;

namespace KnightliaoPikaQ.Tests.Original
{
    // Simulate DB class used in tests (with constant)
    public static class DB
    {
        public const string DB_NAME = "pikaqDemoWeb";
    }

    public class DBTest
    {
        [Fact]
        public void TestDBNameConstant()
        {
            Assert.Equal("pikaqDemoWeb", DB.DB_NAME);
        }
    }
}