using System;
using Xunit;

namespace cyfonly_FLogger.Tests.Public
{
    public class LogFileItemPublicTest
    {
        [Fact]
        public void TestLogFileItemFieldsWithDifferentData()
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

            // Add different test values
            lfi.alLogBufA.Add(new System.Text.StringBuilder("public test AAA"));
            lfi.alLogBufB.Add(new System.Text.StringBuilder("public test BBB"));
            lfi.alLogBufA.Add(new System.Text.StringBuilder("extra item in A"));
            Assert.Equal(2, lfi.alLogBufA.Count);
            Assert.Equal(1, lfi.alLogBufB.Count);
            Assert.Equal("public test AAA", lfi.alLogBufA[0].ToString());
            Assert.Equal("public test BBB", lfi.alLogBufB[0].ToString());
            Assert.Equal("extra item in A", lfi.alLogBufA[1].ToString());
        }
    }
}