using System;
using Xunit;
using ClippingBasicSample.Log;

namespace ClippingBasicSample.Tests.Public
{
    public class LogPublicTest
    {
        private class TestLogNode : ILogNode
        {
            public int Priority;
            public string Tag;
            public string Msg;
            public Exception Tr;

            public void Println(int priority, string tag, string msg, Exception tr)
            {
                Priority = priority;
                Tag = tag;
                Msg = msg;
                Tr = tr;
            }
        }

        private TestLogNode _testNode;

        public LogPublicTest()
        {
            _testNode = new TestLogNode();
            Log.SetLogNode(_testNode);
        }

        [Fact]
        public void TestSetAndGetLogNodePublic()
        {
            Log.SetLogNode(_testNode);
            Assert.Equal(_testNode, Log.GetLogNode());
        }

        [Fact]
        public void TestPrintlnWithThrowablePublic()
        {
            var tr = new ArgumentException("PublicException");
            Log.Println(Log.ERROR, "PUB", "public_msg", tr);
            Assert.Equal(Log.ERROR, _testNode.Priority);
            Assert.Equal("PUB", _testNode.Tag);
            Assert.Equal("public_msg", _testNode.Msg);
            Assert.Equal(tr, _testNode.Tr);
        }

        [Fact]
        public void TestPrintlnWithoutThrowablePublic()
        {
            Log.Println(Log.WARN, "PUB2", "public_msg2");
            Assert.Equal(Log.WARN, _testNode.Priority);
            Assert.Equal("PUB2", _testNode.Tag);
            Assert.Equal("public_msg2", _testNode.Msg);
            Assert.Null(_testNode.Tr);
        }

        [Fact]
        public void TestLevelShortcutsPublic()
        {
            Log.V("PUBv", "visible");
            Assert.Equal(Log.VERBOSE, _testNode.Priority);
            Log.D("PUBd", "debugging");
            Assert.Equal(Log.DEBUG, _testNode.Priority);
            Log.I("PUBi", "information");
            Assert.Equal(Log.INFO, _testNode.Priority);
            Log.W("PUBw", "warning");
            Assert.Equal(Log.WARN, _testNode.Priority);
            Log.E("PUBe", "error occurred", new InvalidOperationException());
            Assert.Equal(Log.ERROR, _testNode.Priority);
            Log.Wtf("PUBa", "assertion");
            Assert.Equal(Log.ASSERT, _testNode.Priority);
        }

        [Fact]
        public void TestNoLogNodeSetPublic()
        {
            Log.SetLogNode(null);
            // Should not throw even if node is null
            Log.Println(Log.INFO, "PUB", "public_msg", null);
        }
    }
}