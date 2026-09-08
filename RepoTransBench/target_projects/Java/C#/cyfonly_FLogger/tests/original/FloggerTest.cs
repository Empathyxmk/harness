using System;
using cyfonly_FLogger;
using cyfonly_FLogger.constants;

namespace cyfonly_FLogger.Tests.Original
{
    public class FloggerTest
    {
        public static void Main(string[] args)
        {
            // 获取单例
            var logger = cyfonly_FLogger.FLogger.GetInstance();
            // 简便api,只需指定内容
            logger.Info("Here is your message...");
            // 指定日志级别和内容，文件名自动映射
            logger.WriteLog(Constant.INFO, "Here is your customized level message...");
            // 指定日志输出文件名、日志级别和内容
            logger.WriteLog("error", Constant.ERROR, "Here is your customized log file and level message...");
        }
    }
}