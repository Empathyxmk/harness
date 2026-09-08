using Xunit;

namespace cyfonly_FLogger.Tests.Public
{
    public class ConstantPublicTest
    {
        [Fact]
        public void TestLevelsAndMapPublic()
        {
            Assert.Equal(4, cyfonly_FLogger.constants.Constant.FATAL);
            Assert.Equal("FATAL", cyfonly_FLogger.constants.Constant.LOG_DESC_MAP["4"]);
            Assert.Equal("DEBUG", cyfonly_FLogger.constants.Constant.LOG_DESC_MAP["0"]);
            Assert.NotNull(cyfonly_FLogger.constants.Constant.CFG_LOG_LEVEL);
            Assert.Contains("4", cyfonly_FLogger.constants.Constant.CFG_LOG_LEVEL);
        }

        [Fact]
        public void TestCharsetAndPathPublic()
        {
            Assert.NotNull(cyfonly_FLogger.constants.Constant.CFG_CHARSET_NAME);
            Assert.NotNull(cyfonly_FLogger.constants.Constant.CFG_LOG_PATH);
            Assert.Contains("UTF", cyfonly_FLogger.constants.Constant.CFG_CHARSET_NAME.ToUpper());
            Assert.Contains("log", cyfonly_FLogger.constants.Constant.CFG_LOG_PATH);
        }
    }
}