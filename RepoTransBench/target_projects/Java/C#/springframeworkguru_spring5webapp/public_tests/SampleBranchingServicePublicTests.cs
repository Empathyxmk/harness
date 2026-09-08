using Xunit;
using Spring5Webapp;

namespace Spring5Webapp.PublicTests
{
    public class SampleBranchingServicePublicTests
    {
        private readonly SampleBranchingService service = new SampleBranchingService();

        [Fact]
        public void TestCategorizeNegativePublic()
        {
            Assert.Equal("negative", service.CategorizeNumber(-15));
        }

        [Fact]
        public void TestCategorizeZeroPublic()
        {
            Assert.Equal("zero", service.CategorizeNumber(0));
        }

        [Fact]
        public void TestCategorizeSmallPublic()
        {
            Assert.Equal("small", service.CategorizeNumber(8));
        }

        [Fact]
        public void TestCategorizeLargePublic()
        {
            Assert.Equal("large", service.CategorizeNumber(50));
        }

        [Fact]
        public void TestIsEvenTruePublic()
        {
            Assert.True(service.IsEven(6));
        }

        [Fact]
        public void TestIsEvenFalsePublic()
        {
            Assert.False(service.IsEven(9));
        }
    }
}