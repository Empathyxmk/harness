using Xunit;
using Moq;
using SlidingTabsBasic.Common.Logger;
using System;

namespace OriginalTests
{
    public class LogTests : IDisposable
    {
        private Mock<LogNode> mockNode;

        public LogTests()
        {
            mockNode = new Mock<LogNode>();
            Log.SetLogNode(mockNode.Object);
        }

        public void Dispose()
        {
            Log.SetLogNode(null);
        }

        [Fact]
        public void TestSetAndGetLogNode()
        {
            Assert.Equal(mockNode.Object, Log.GetLogNode());
        }

        [Fact]
        public void TestPrintlnCallsNode()
        {
            Log.Println(Log.DEBUG, "TAG", "msg", null);
            mockNode.Verify(m => m.Println(Log.DEBUG, "TAG", "msg", null));

            Log.Println(Log.INFO, "TAG2", "msg2");
            mockNode.Verify(m => m.Println(Log.INFO, "TAG2", "msg2", null));
        }

        [Fact]
        public void TestVerbosityDelegates()
        {
            Log.V("V", "verbose");
            mockNode.Verify(m => m.Println(Log.VERBOSE, "V", "verbose", null));
            Log.V("V2", "verbose2", It.IsAny<Exception>());
            Log.V("V2", "verbose2", new Exception("err"));
            mockNode.Verify(m => m.Println(Log.VERBOSE, "V2", "verbose2", It.IsAny<Exception>()));
        }

        [Fact]
        public void TestDebugDelegates()
        {
            Log.D("D", "debug");
            mockNode.Verify(m => m.Println(Log.DEBUG, "D", "debug", null));
            Log.D("D2", "debug2", new Exception("err"));
            mockNode.Verify(m => m.Println(Log.DEBUG, "D2", "debug2", It.IsAny<Exception>()));
        }

        [Fact]
        public void TestInfoDelegates()
        {
            Log.I("I", "info");
            mockNode.Verify(m => m.Println(Log.INFO, "I", "info", null));
            Log.I("I2", "info2", new Exception("err"));
            mockNode.Verify(m => m.Println(Log.INFO, "I2", "info2", It.IsAny<Exception>()));
        }

        [Fact]
        public void TestWarnDelegates()
        {
            Log.W("W", "warn");
            mockNode.Verify(m => m.Println(Log.WARN, "W", "warn", null));
            Log.W("W2", "warn2", new Exception("err"));
            mockNode.Verify(m => m.Println(Log.WARN, "W2", "warn2", It.IsAny<Exception>()));
        }

        [Fact]
        public void TestErrorDelegates()
        {
            Log.E("E", "error");
            mockNode.Verify(m => m.Println(Log.ERROR, "E", "error", null));
            Log.E("E2", "error2", new Exception("err"));
            mockNode.Verify(m => m.Println(Log.ERROR, "E2", "error2", It.IsAny<Exception>()));
        }

        [Fact]
        public void TestWtfDelegates()
        {
            Log.Wtf("T", "assert");
            mockNode.Verify(m => m.Println(Log.ASSERT, "T", "assert", null));
            Log.Wtf("T2", "assert2", new Exception("err"));
            mockNode.Verify(m => m.Println(Log.ASSERT, "T2", "assert2", It.IsAny<Exception>()));
        }

        [Fact]
        public void TestNoNodeDoesNotCrash()
        {
            Log.SetLogNode(null);
            Log.D("TAG", "Should do nothing");
        }
    }
}