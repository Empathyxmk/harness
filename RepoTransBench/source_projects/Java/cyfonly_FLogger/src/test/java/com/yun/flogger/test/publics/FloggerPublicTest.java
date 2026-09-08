package com.yun.flogger.test.publics;

import com.cyfonly.flogger.FLogger;
import com.cyfonly.flogger.constants.Constant;

public class FloggerPublicTest {

    public static void main(String[] args) {
        // 获取单例
        FLogger logger = FLogger.getInstance();
        // 使用不同消息内容进行测试
        logger.info("This is a public test info message!");
        logger.writeLog(Constant.WARN, "This is a public customized level message!");
        logger.writeLog("custom_public", Constant.DEBUG, "This is a public custom log file and debug level message!");
        // extra logs to test other levels
        logger.warn("Public test warning log");
        logger.error("Public test error log");
    }
}