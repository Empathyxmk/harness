using Xunit;
using NetEaseArrow;

namespace NetEaseArrowTests.Public
{
    public class NeXMLReporterConfigPublicTests
    {
        [Fact]
        public void TestConfigConstantsWithDifferentAccessPattern()
        {
            // Same constants, different order/style of assertions for coverage
            Assert.True(NeXMLReporterConfig.ATTR_AUTHOR == "author");
            Assert.Equal("testName", NeXMLReporterConfig.ATTR_TC_NAME);
            Assert.Equal("suiteName", NeXMLReporterConfig.ATTR_TC_SUITES);
        }
    }
}