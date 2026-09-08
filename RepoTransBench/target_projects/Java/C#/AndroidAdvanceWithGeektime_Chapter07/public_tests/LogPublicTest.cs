using System;
using Xunit;
using SystraceGradlePlugin;

namespace PublicTests
{
    public class LogPublicTest
    {
        private class PublicTestLogImp : ILogImp
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

        public LogPublicTest()
        {
            _original = Log.GetImpl();
        }
        ~LogPublicTest()
        {
            Log.SetLogImp(_original);
        }

        [Fact]
        public void TestSetAndGetImplPublic()
        {
            var imp = new PublicTestLogImp();
            Log.SetLogImp(imp);
            Assert.Equal(imp, Log.GetImpl());
        }

        [Fact]
        public void TestLogMethodsDelegateToImplPublic()
        {
            var imp = new PublicTestLogImp();
            Log.SetLogImp(imp);

            Log.V("PUB", "Verbose log {0}", 10);
            Log.I("PUB", "Info log");
            Log.W("PUB", "Warning {0}", 24);
            Log.D("PUB", "Debug message");
            Log.E("PUB", "Error string {0}", "oops");

            var t = new ArgumentException("public error");
            Log.PrintErrStackTrace("PUB", t, "formatting {0}", "msg2");
            Assert.True(imp.VCalled);
            Assert.True(imp.ICalled);
            Assert.True(imp.WCalled);
            Assert.True(imp.DCalled);
            Assert.True(imp.ECalled);
            Assert.True(imp.ErrStackTraceCalled);
            Assert.Equal(t, imp.LastTr);
            Assert.Equal("PUB", imp.LastTag);
        }

        [Fact]
        public void TestNullImplDoesNotThrowPublic()
        {
            Log.SetLogImp(null);
            Log.V("PUB", "message");
            Log.D("PUB", "message");
            Log.I("PUB", "message");
            Log.W("PUB", "message");
            Log.E("PUB", "message");
            Log.PrintErrStackTrace("PUB", new Exception("public error"), "message");
        }
    }
}