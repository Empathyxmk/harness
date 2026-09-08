using Xunit;
using Spring5Webapp;

namespace Spring5Webapp.Tests.Original
{
    public class SampleBranchingServiceTests
    {
        private readonly SampleBranchingService service = new SampleBranchingService();

        [Fact]
        public void TestCategorizeNegative()
        {
            Assert.Equal("negative", service.CategorizeNumber(-5));
        }

        [Fact]
        public void TestCategorizeZero()
        {
            Assert.Equal("zero", service.CategorizeNumber(0));
        }

        [Fact]
        public void TestCategorizeSmall()
        {
            Assert.Equal("small", service.CategorizeNumber(5));
        }

        [Fact]
        public void TestCategorizeLarge()
        {
            Assert.Equal("large", service.CategorizeNumber(100));
        }

        [Fact]
        public void TestIsEvenTrue()
        {
            Assert.True(service.IsEven(2));
        }

        [Fact]
        public void TestIsEvenFalse()
        {
            Assert.False(service.IsEven(3));
        }
    }
}