using Xunit;
using yacy_yacy_grid_crawler.coverage;

namespace yacy_yacy_grid_crawler.public_tests
{
    public class DemoCoveragePublicTests
    {
        [Fact]
        public void TestAddOne_Public()
        {
            int result = DemoCoverage.addOne(42);
            Assert.Equal(43, result);
        }

        [Fact]
        public void TestSubtractOne_Public()
        {
            int result = DemoCoverage.subtractOne(12);
            Assert.Equal(11, result);
        }

        [Fact]
        public void TestAddOneWithNegativeValue_Public()
        {
            int result = DemoCoverage.addOne(-7);
            Assert.Equal(-6, result);
        }
    }
}