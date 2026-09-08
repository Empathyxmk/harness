using System;
using Xunit;
using SystraceGradlePlugin;

namespace TestsOriginal
{
    public class LogTest
    {
        private class TestLogImp : ILogImp
        {
            public bool VCalled, ICalled, WCalled, DCalled, ECalled, ErrStackTraceCalled;
            public string LastTag, LastMsg;
            public object[] LastObj;
            public Exception LastTr;
            public string LastFormat;

            public void V(string tag, string msg, params object[] obj)
            {
                VCalled = true; LastTag = tag; LastMsg = msg; LastObj = obj;
            }
            public void I(string tag, string msg, params object[] obj)
            {
                ICalled = true; LastTag = tag; LastMsg = msg; LastObj = obj;
            }
            public void W(string tag, string msg, params object[] obj)
            {
                WCalled = true; LastTag = tag; LastMsg = msg; LastObj = obj;
            }
            public void D(string tag, string msg, params object[] obj)
            {
                DCalled = true; LastTag = tag; LastMsg = msg; LastObj = obj;
            }
            public void E(string tag, string msg, params object[] obj)
            {
                ECalled = true; LastTag = tag; LastMsg = msg; LastObj = obj;
            }
            public void PrintErrStackTrace(string tag, Exception tr, string format, params object[] obj)
            {
                ErrStackTraceCalled = true; LastTag = tag; LastMsg = null; LastTr = tr; LastFormat = format; LastObj = obj;
            }
        }

        private ILogImp _original;

        public LogTest()
        {
            _original = Log.GetImpl();
        }
        ~LogTest()
        {
            Log.SetLogImp(_original);
        }

        [Fact]
        public void TestSetAndGetImpl()
        {
            var imp = new TestLogImp();
            Log.SetLogImp(imp);
            Assert.Equal(imp, Log.GetImpl());
        }

        [Fact]
        public void TestLogMethodsDelegateToImpl()
        {
            var imp = new TestLogImp();
            Log.SetLogImp(imp);

            Log.V("TAG", "Ver msg {0}", 1);
            Log.I("TAG", "Info msg");
            Log.W("TAG", "Warn {0}", 42);
            Log.D("TAG", "Dbg");
            Log.E("TAG", "Err {0}", "msg");

            var t = new Exception("err");
            Log.PrintErrStackTrace("TAG", t, "format {0}", "err");
            Assert.True(imp.VCalled);
            Assert.True(imp.ICalled);
            Assert.True(imp.WCalled);
            Assert.True(imp.DCalled);
            Assert.True(imp.ECalled);
            Assert.True(imp.ErrStackTraceCalled);
            Assert.Equal(t, imp.LastTr);
            Assert.Equal("TAG", imp.LastTag);
        }

        [Fact]
        public void TestNullImplDoesNotThrow()
        {
            Log.SetLogImp(null);
            Log.V("TAG", "msg");
            Log.D("TAG", "msg");
            Log.I("TAG", "msg");
            Log.W("TAG", "msg");
            Log.E("TAG", "msg");
            Log.PrintErrStackTrace("TAG", new Exception("err"), "msg");
        }
    }
}