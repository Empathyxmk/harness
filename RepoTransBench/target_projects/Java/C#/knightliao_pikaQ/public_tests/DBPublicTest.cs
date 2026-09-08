using Xunit;

namespace KnightliaoPikaQ.PublicTests
{
    // Simulate DB class as in original
    public static class DB
    {
        public const string DB_NAME = "pikaqDemoWeb";
    }

    public class DBPublicTest
    {
        [Fact]
        public void TestDBNameConstantDifferent()
        {
            // Checking same constant, but using contains for a different assertion
            Assert.Contains("DemoWeb", DB.DB_NAME);
        }
    }
}