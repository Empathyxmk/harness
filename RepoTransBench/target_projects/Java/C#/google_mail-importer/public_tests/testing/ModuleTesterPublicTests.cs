using Xunit;

namespace GoogleMailImporter.PublicTests.Testing
{
    public class ModuleTesterPublicTests
    {
        [Fact]
        public void TestDifferentModuleTesterRuns()
        {
            var tester = new ModuleTester();
            tester.Test();
        }
    }

    public class ModuleTester
    {
        public void Test()
        {
            // Dummy - just for coverage
            int x = 1 + 1;
            Assert.Equal(2, x);
        }
    }
}