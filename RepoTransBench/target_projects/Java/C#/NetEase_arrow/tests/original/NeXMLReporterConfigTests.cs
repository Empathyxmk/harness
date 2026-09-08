using Xunit;
using NetEaseArrow;

namespace NetEaseArrowTests.Original
{
    public class NeXMLReporterConfigTests
    {
        [Fact]
        public void TestConfigConstants()
        {
            Assert.Equal("testName", NeXMLReporterConfig.ATTR_TC_NAME);
            Assert.Equal("suiteName", NeXMLReporterConfig.ATTR_TC_SUITES);
            Assert.Equal("author", NeXMLReporterConfig.ATTR_AUTHOR);
        }
    }
}