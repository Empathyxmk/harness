using Xunit;

namespace cyfonly_FLogger.Tests.Original
{
    public class FLoggerCoreTest
    {
        [Fact]
        public void TestDebugInfoWarnErrorFatal()
        {
            var logger = cyfonly_FLogger.FLogger.GetInstance();
            logger.Debug("debug test message");
            logger.Info("info test message");
            logger.Warn("warn test message");
            logger.Error("error test message");
            logger.Fatal("fatal test message");
        }

        [Fact]
        public void TestWriteLogWithLevel()
        {
            var logger = cyfonly_FLogger.FLogger.GetInstance();
            logger.WriteLog(cyfonly_FLogger.constants.Constant.DEBUG, "level debug");
            logger.WriteLog(cyfonly_FLogger.constants.Constant.INFO, "level info");
            logger.WriteLog(cyfonly_FLogger.constants.Constant.WARN, "level warn");
            logger.WriteLog(cyfonly_FLogger.constants.Constant.ERROR, "level error");
            logger.WriteLog(cyfonly_FLogger.constants.Constant.FATAL, "level fatal");
        }

        [Fact]
        public void TestWriteLogNullAndBelowLevel()
        {
            var logger = cyfonly_FLogger.FLogger.GetInstance();
            logger.WriteLog("testfile", cyfonly_FLogger.constants.Constant.DEBUG, null); // null should not throw

            var oldLevel = cyfonly_FLogger.constants.Constant.CFG_LOG_LEVEL;
            cyfonly_FLogger.constants.Constant.CFG_LOG_LEVEL = ""; // disable all
            logger.WriteLog("shouldSkip", cyfonly_FLogger.constants.Constant.DEBUG, "skip this");
            cyfonly_FLogger.constants.Constant.CFG_LOG_LEVEL = oldLevel;
        }
    }
}