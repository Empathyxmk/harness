using System;
using Xunit;
using ClippingBasicSample.Log;

namespace ClippingBasicSample.Tests.Public
{
    public class MessageOnlyLogFilterPublicTest
    {
        private class RecordingNode : ILogNode
        {
            public int LastPriority = int.MaxValue;
            public string LastTag = "abc";
            public string LastMsg = "zzz";
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

        public MessageOnlyLogFilterPublicTest()
        {
            _recorder = new RecordingNode();
            _filter = new MessageOnlyLogFilter();
            _filter.SetNext(_recorder);
        }

        [Fact]
        public void TestPrintlnFiltersToMessageOnlyPublic()
        {
            _filter.Println(Log.WARN, "PUBTAG", "public message", new Exception("not seen"));
            Assert.Equal(Log.NONE, _recorder.LastPriority);
            Assert.Null(_recorder.LastTag);
            Assert.Equal("public message", _recorder.LastMsg);
            Assert.Null(_recorder.LastTr);
        }

        [Fact]
        public void TestConstructorWithNextPublic()
        {
            var f2 = new MessageOnlyLogFilter(_recorder);
            Assert.Equal(_recorder, f2.GetNext());
        }

        [Fact]
        public void TestSetAndGetNextPublic()
        {
            var f3 = new MessageOnlyLogFilter();
            f3.SetNext(_recorder);
            Assert.Equal(_recorder, f3.GetNext());
        }

        [Fact]
        public void TestNullNextDoesNothingPublic()
        {
            var f4 = new MessageOnlyLogFilter();
            // Should not throw
            f4.Println(Log.VERBOSE, "v", "pqrs", null);
        }
    }
}