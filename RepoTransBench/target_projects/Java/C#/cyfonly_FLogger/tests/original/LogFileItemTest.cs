using System;
using System.Collections.Generic;
using Xunit;

namespace cyfonly_FLogger.Tests.Original
{
    // Needs reference to cyfonly_FLogger/src, especially LogFileItem.
    public class LogFileItemTest
    {
        [Fact]
        public void TestLogFileItemFields()
        {
            var lfi = new cyfonly_FLogger.strategy.LogFileItem();
            Assert.Equal("", lfi.logFileName);
            Assert.Equal("", lfi.fullLogFileName);
            Assert.Equal(0, lfi.currLogSize);
            Assert.Equal('A', lfi.currLogBuff);
            Assert.NotNull(lfi.alLogBufA);
            Assert.NotNull(lfi.alLogBufB);
            Assert.True(lfi.alLogBufA.Count == 0);
            Assert.True(lfi.alLogBufB.Count == 0);
            Assert.Equal(0, lfi.nextWriteTime);
            Assert.Equal("", lfi.lastPCDate);
            Assert.Equal(0, lfi.currCacheSize);

            lfi.alLogBufA.Add(new System.Text.StringBuilder("test A"));
            lfi.alLogBufB.Add(new System.Text.StringBuilder("test B"));
            Assert.Equal(1, lfi.alLogBufA.Count);
            Assert.Equal(1, lfi.alLogBufB.Count);
        }
    }
}