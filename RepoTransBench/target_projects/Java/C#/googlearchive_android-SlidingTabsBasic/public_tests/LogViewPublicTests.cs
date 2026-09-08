using Xunit;
using Moq;
using SlidingTabsBasic.Common.Logger;
using System.Text;
using System;

namespace PublicTests
{
    public class LogViewPublicTests
    {
        private class DummyActivity
        {
            public void RunOnUiThread(Action runnable) => runnable();
        }

        [Fact]
        public void TestAllConstructors()
        {
            var ctx = new object();
            var attrs = new object();

            var v1 = new LogView(ctx);
            var v2 = new LogView(ctx, attrs);
            var v3 = new LogView(ctx, attrs, 2);

            Assert.NotNull(v1);
            Assert.NotNull(v2);
            Assert.NotNull(v3);
        }

        [Fact]
        public void TestAppendIfNotNullEdgeCases()
        {
            var ctx = new object();
            var v = new LogView(ctx);

            StringBuilder sb = new StringBuilder("public");
            var mi = typeof(LogView).GetMethod("AppendIfNotNull", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);
            var sb2 = (StringBuilder)mi.Invoke(v, new object[] { sb, "append", "|" });
            Assert.Equal("publicappend|", sb2.ToString());

            sb = new StringBuilder("q");
            sb2 = (StringBuilder)mi.Invoke(v, new object[] { sb, "", "|" });
            Assert.Equal("q", sb2.ToString());

            sb = new StringBuilder();
            sb2 = (StringBuilder)mi.Invoke(v, new object[] { sb, null, ";" });
            Assert.Equal("", sb2.ToString());
        }

        [Fact]
        public void TestPrintlnWithPublicData()
        {
            var ctx = new DummyActivity();
            var v = new Mock<LogView>(ctx) { CallBase = true };
            string output = null;
            v.Setup(x => x.AppendToLog(It.IsAny<string>())).Callback<string>(s => output = s);

            v.Object.Println(Log.INFO, "tagPublic1", "msgInfo", null);

            Assert.Contains("INFO", output);
            Assert.Contains("tagPublic1", output);
            Assert.Contains("msgInfo", output);

            Exception t = new ArgumentException("InvalidArg");
            v.Object.Println(Log.DEBUG, "tagPublic2", "msgDebug", t);
            Assert.Contains("DEBUG", output);
            Assert.Contains("msgDebug", output);
            Assert.Contains("ArgumentException", output);

            var next = new Mock<LogNode>();
            v.Object.SetNext(next.Object);
            v.Object.Println(Log.VERBOSE, "tagP", "msgP", null);
            next.Verify(n => n.Println(It.IsAny<int>(), It.IsAny<string>(), It.IsAny<string>(), It.IsAny<Exception>()));
        }

        [Fact]
        public void TestSetGetNextNodePublic()
        {
            var ctx = new object();
            var v = new LogView(ctx);
            Assert.Null(v.GetNext());
            var ln = new Mock<LogNode>();
            v.SetNext(ln.Object);
            Assert.Equal(ln.Object, v.GetNext());
        }
    }
}