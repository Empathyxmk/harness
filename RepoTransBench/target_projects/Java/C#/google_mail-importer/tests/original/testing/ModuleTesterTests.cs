using Xunit;

namespace GoogleMailImporter.Tests.Original.Testing
{
    public class ModuleTesterTests
    {
        [Fact]
        public void ModuleTesterRuns()
        {
            var tester = new ModuleTester();
            tester.Test();
        }
    }

    public class ModuleTester
    {
        public void Test()
        {
            int x = 2 * 2;
            Assert.Equal(4, x);
        }
    }
}