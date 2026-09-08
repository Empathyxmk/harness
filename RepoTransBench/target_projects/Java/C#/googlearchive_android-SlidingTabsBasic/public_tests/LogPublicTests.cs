using Xunit;
using Moq;
using SlidingTabsBasic.Common.Logger;
using System;

namespace PublicTests
{
    public class LogPublicTests : IDisposable
    {
        private Mock<LogNode> mockNode;

        public LogPublicTests()
        {
            mockNode = new Mock<LogNode>();
            Log.SetLogNode(mockNode.Object);
        }

        public void Dispose()
        {
            Log.SetLogNode(null);
        }

        [Fact]
        public void TestSetAndGetLogNodePublic()
        {
            Assert.Equal(mockNode.Object, Log.GetLogNode());
        }

        [Fact]
        public void TestPrintlnCallsNodeWithDifferentValues()
        {
            Log.Println(Log.INFO, "PUB_TAG", "publicMsg", null);
            mockNode.Verify(m => m.Println(Log.INFO, "PUB_TAG", "publicMsg", null));

            Log.Println(Log.WARN, "PUB_TAG_WARN", "warnMsg");
            mockNode.Verify(m => m.Println(Log.WARN, "PUB_TAG_WARN", "warnMsg", null));
        }

        [Fact]
        public void TestVerboseDelegatesWithDifferentInput()
        {
            Log.V("VerboseTag", "verbMsg");
            mockNode.Verify(m => m.Println(Log.VERBOSE, "VerboseTag", "verbMsg", null));

            Log.V("VerbTag2", "verbMsg2", new ArgumentException("public"));
            mockNode.Verify(m => m.Println(Log.VERBOSE, "VerbTag2", "verbMsg2", It.IsAny<Exception>()));
        }

        [Fact]
        public void TestDebugDelegatesWithDifferentInput()
        {
            Log.D("DebugTag", "debugMessage");
            mockNode.Verify(m => m.Println(Log.DEBUG, "DebugTag", "debugMessage", null));

            Log.D("DebugTag2", "debugMessage2", new InvalidOperationException("failure"));
            mockNode.Verify(m => m.Println(Log.DEBUG, "DebugTag2", "debugMessage2", It.IsAny<Exception>()));
        }

        [Fact]
        public void TestInfoDelegatesWithPublicData()
        {
            Log.I("InfoTag", "infoMsg1");
            mockNode.Verify(m => m.Println(Log.INFO, "InfoTag", "infoMsg1", null));

            Log.I("InfoTag2", "infoMsg2", new NullReferenceException("infoNull"));
            mockNode.Verify(m => m.Println(Log.INFO, "InfoTag2", "infoMsg2", It.IsAny<Exception>()));
        }

        [Fact]
        public void TestWarnDelegatesPublic()
        {
            Log.W("WarnTag", "warnMsg1");
            mockNode.Verify(m => m.Println(Log.WARN, "WarnTag", "warnMsg1", null));

            Log.W("WarnTag2", "warnMsg2", new ArithmeticException("warnArith"));
            mockNode.Verify(m => m.Println(Log.WARN, "WarnTag2", "warnMsg2", It.IsAny<Exception>()));
        }

        [Fact]
        public void TestErrorDelegatesPublic()
        {
            Log.E("ErrorTag", "errorMsg1");
            mockNode.Verify(m => m.Println(Log.ERROR, "ErrorTag", "errorMsg1", null));

            Log.E("ErrorTag2", "errorMsg2", new Exception("publicError"));
            mockNode.Verify(m => m.Println(Log.ERROR, "ErrorTag2", "errorMsg2", It.IsAny<Exception>()));
        }

        [Fact]
        public void TestWtfDelegatesWithDifferentData()
        {
            Log.Wtf("AssertT", "assertMsg");
            mockNode.Verify(m => m.Println(Log.ASSERT, "AssertT", "assertMsg", null));

            Log.Wtf("AssertT2", "assertMsg2", new Exception("assertThrowable"));
            mockNode.Verify(m => m.Println(Log.ASSERT, "AssertT2", "assertMsg2", It.IsAny<Exception>()));
        }

        [Fact]
        public void TestNoNodeSafeOnNullPublic()
        {
            Log.SetLogNode(null);
            Log.I("SafeTAG", "ShouldBeSafe");
        }
    }
}