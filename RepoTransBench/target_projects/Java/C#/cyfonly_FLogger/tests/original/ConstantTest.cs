using Xunit;

namespace cyfonly_FLogger.Tests.Original
{
    public class ConstantTest
    {
        [Fact]
        public void TestLogLevels()
        {
            Assert.Equal(0, cyfonly_FLogger.constants.Constant.DEBUG);
            Assert.Equal(1, cyfonly_FLogger.constants.Constant.INFO);
            Assert.Equal(2, cyfonly_FLogger.constants.Constant.WARN);
            Assert.Equal(3, cyfonly_FLogger.constants.Constant.ERROR);
            Assert.Equal(4, cyfonly_FLogger.constants.Constant.FATAL);
        }

        [Fact]
        public void TestLogDescMap()
        {
            Assert.Equal("DEBUG", cyfonly_FLogger.constants.Constant.LOG_DESC_MAP["0"]);
            Assert.Equal("INFO", cyfonly_FLogger.constants.Constant.LOG_DESC_MAP["1"]);
            Assert.Equal("WARN", cyfonly_FLogger.constants.Constant.LOG_DESC_MAP["2"]);
            Assert.Equal("ERROR", cyfonly_FLogger.constants.Constant.LOG_DESC_MAP["3"]);
            Assert.Equal("FATAL", cyfonly_FLogger.constants.Constant.LOG_DESC_MAP["4"]);
        }

        [Fact]
        public void TestConfigDefaults()
        {
            Assert.NotNull(cyfonly_FLogger.constants.Constant.CFG_LOG_LEVEL);
            Assert.True(cyfonly_FLogger.constants.Constant.CFG_CHARSET_NAME.Equals("UTF-8", System.StringComparison.OrdinalIgnoreCase));
            Assert.False(string.IsNullOrEmpty(cyfonly_FLogger.constants.Constant.CFG_LOG_PATH));
        }
    }
}