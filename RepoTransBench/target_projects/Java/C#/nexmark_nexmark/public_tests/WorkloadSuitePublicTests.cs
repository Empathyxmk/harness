using System;
using Xunit;
using NexmarkFlink.workload;

namespace PublicTests
{
    public class WorkloadSuitePublicTests
    {
        [Fact]
        public void TestFromCategoryQueryNamePublic()
        {
            var suite = WorkloadSuite.FromCategoryQueryName("cep", "q2");
            Assert.NotNull(suite);
            Assert.NotEmpty(suite.SuiteList());
            Assert.Equal("q2", suite.SuiteList()[0].QueryName);
            Assert.Equal("cep", suite.SuiteList()[0].Category);
        }

        [Fact]
        public void TestFromCategoryQueryNameAllPublic()
        {
            var suite = WorkloadSuite.FromCategoryQueryName("oa", "all");
            Assert.NotNull(suite);
            Assert.True(suite.SuiteList().Count > 5);
        }
    }
}