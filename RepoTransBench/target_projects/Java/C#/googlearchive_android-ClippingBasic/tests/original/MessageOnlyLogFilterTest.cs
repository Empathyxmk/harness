using System;
using Xunit;
using ClippingBasicSample.Log;

namespace ClippingBasicSample.Tests.Original
{
    public class MessageOnlyLogFilterTest
    {
        private class RecordingNode : ILogNode
        {
            public int LastPriority = int.MinValue;
            public string LastTag = "zzz";
            public string LastMsg = "uuu";
            public Exception LastTr;

            public void Println(int priority, string tag, string msg, Exception tr)
            {
                LastPriority = priority;
                LastTag = tag;
                LastMsg = msg;
                LastTr = tr;
            }
        }

        private MessageOnlyLogFilter _filter;
        private RecordingNode _recorder;

        public MessageOnlyLogFilterTest()
        {
            _recorder = new RecordingNode();
            _filter = new MessageOnlyLogFilter();
            _filter.SetNext(_recorder);
        }

        [Fact]
        public void TestPrintlnFiltersToMessageOnly()
        {
            _filter.Println(Log.INFO, "TAG", "hellomsg", new Exception("should not propagate"));
            Assert.Equal(Log.NONE, _recorder.LastPriority);
            Assert.Null(_recorder.LastTag);
            Assert.Equal("hellomsg", _recorder.LastMsg);
            Assert.Null(_recorder.LastTr);
        }

        [Fact]
        public void TestConstructorWithNext()
        {
            var f2 = new MessageOnlyLogFilter(_recorder);
            Assert.Equal(_recorder, f2.GetNext());
        }

        [Fact]
        public void TestSetAndGetNext()
        {
            var f3 = new MessageOnlyLogFilter();
            f3.SetNext(_recorder);
            Assert.Equal(_recorder, f3.GetNext());
        }

        [Fact]
        public void TestNullNextDoesNothing()
        {
            var f4 = new MessageOnlyLogFilter();
            // Should not throw
            f4.Println(Log.ERROR, "x", "yz", null);
        }
    }
}