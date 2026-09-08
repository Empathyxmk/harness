using System;
using System.Collections.Generic;
using Xunit;
using NexmarkFlink.workload;
using Microsoft.Extensions.Configuration;

namespace OriginalTests
{
    public class WorkloadSuiteTests
    {
        [Fact]
        public void TestEqualsAndHashCode()
        {
            var suite1 = new WorkloadSuite(new Dictionary<string, object>());
            var suite2 = new WorkloadSuite(new Dictionary<string, object>());
            Assert.Equal(suite1, suite2);
            Assert.Equal(suite1.GetHashCode(), suite2.GetHashCode());
        }

        [Fact]
        public void TestToString()
        {
            var suite = new WorkloadSuite(new Dictionary<string, object>());
            Assert.Contains("query2Workload", suite.ToString());
        }

        [Fact]
        public void TestFromConfReturnsSuite()
        {
            var builder = new ConfigurationBuilder();
            var conf = new Dictionary<string, string>
            {
                { "nexmark.workload.suite.s1.queries", "q1" },
                { "nexmark.workload.suite.s1.tps", "1000" },
                { "nexmark.workload.suite.s1.events.num", "10000" }
            };
            builder.AddInMemoryCollection(conf);
            var configuration = builder.Build();

            var suite = WorkloadSuite.FromConf(configuration, "oa");
            Assert.NotNull(suite);
            Assert.NotNull(suite.GetQueryWorkload("q1"));
        }
    }
}