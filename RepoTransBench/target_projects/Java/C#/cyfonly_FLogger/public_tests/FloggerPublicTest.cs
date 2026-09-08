using System;
using cyfonly_FLogger;
using cyfonly_FLogger.constants;

namespace cyfonly_FLogger.Tests.Public
{
    public class FloggerPublicTest
    {
        public static void Main(string[] args)
        {
            // 获取单例
            var logger = cyfonly_FLogger.FLogger.GetInstance();
            // 使用不同消息内容进行测试
            logger.Info("This is a public test info message!");
            logger.WriteLog(Constant.WARN, "This is a public customized level message!");
            logger.WriteLog("custom_public", Constant.DEBUG, "This is a public custom log file and debug level message!");
            logger.Warn("Public test warning log");
            logger.Error("Public test error log");
        }
    }
}