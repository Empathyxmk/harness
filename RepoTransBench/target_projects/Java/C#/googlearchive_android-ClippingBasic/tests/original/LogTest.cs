using System;
using Xunit;
using ClippingBasicSample.Log;

namespace ClippingBasicSample.Tests.Original
{
    public class LogTest
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

        public LogTest()
        {
            _testNode = new TestLogNode();
            Log.SetLogNode(_testNode);
        }

        [Fact]
        public void TestSetAndGetLogNode()
        {
            Log.SetLogNode(_testNode);
            Assert.Equal(_testNode, Log.GetLogNode());
        }

        [Fact]
        public void TestPrintlnWithThrowable()
        {
            var tr = new Exception("Exception");
            Log.Println(Log.DEBUG, "TAG", "msg", tr);
            Assert.Equal(Log.DEBUG, _testNode.Priority);
            Assert.Equal("TAG", _testNode.Tag);
            Assert.Equal("msg", _testNode.Msg);
            Assert.Equal(tr, _testNode.Tr);
        }

        [Fact]
        public void TestPrintlnWithoutThrowable()
        {
            Log.Println(Log.INFO, "TAG2", "msg2");
            Assert.Equal(Log.INFO, _testNode.Priority);
            Assert.Equal("TAG2", _testNode.Tag);
            Assert.Equal("msg2", _testNode.Msg);
            Assert.Null(_testNode.Tr);
        }

        [Fact]
        public void TestLevelShortcuts()
        {
            Log.V("TAGv", "verbose");
            Assert.Equal(Log.VERBOSE, _testNode.Priority);
            Log.D("TAGd", "debug");
            Assert.Equal(Log.DEBUG, _testNode.Priority);
            Log.I("TAGi", "info");
            Assert.Equal(Log.INFO, _testNode.Priority);
            Log.W("TAGw", "warn");
            Assert.Equal(Log.WARN, _testNode.Priority);
            Log.E("TAGe", "error", new NullReferenceException());
            Assert.Equal(Log.ERROR, _testNode.Priority);
            Log.Wtf("TAGa", "assert");
            Assert.Equal(Log.ASSERT, _testNode.Priority);
        }

        [Fact]
        public void TestNoLogNodeSet()
        {
            Log.SetLogNode(null);
            // Should not throw even if node is null
            Log.Println(Log.DEBUG, "TAG", "msg", null);
        }
    }
}