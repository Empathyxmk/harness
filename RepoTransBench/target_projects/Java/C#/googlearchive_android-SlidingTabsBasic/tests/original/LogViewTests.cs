using Xunit;
using Moq;
using SlidingTabsBasic.Common.Logger;
using System.Text;
using System;

namespace OriginalTests
{
    public class LogViewTests
    {
        private class DummyActivity
        {
            public void RunOnUiThread(Action runnable) => runnable();
        }

        [Fact]
        public void TestConstructors()
        {
            var ctx = new object();
            var attrs = new object();

            var v1 = new LogView(ctx);
            var v2 = new LogView(ctx, attrs);
            var v3 = new LogView(ctx, attrs, 1);

            Assert.NotNull(v1);
            Assert.NotNull(v2);
            Assert.NotNull(v3);
        }

        [Fact]
        public void TestAppendIfNotNullBehavior()
        {
            var ctx = new object();
            var v = new LogView(ctx);

            StringBuilder sb = new StringBuilder("start");
            var mi = typeof(LogView).GetMethod("AppendIfNotNull", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);
            var sb2 = (StringBuilder)mi.Invoke(v, new object[] { sb, "add", "," });
            Assert.Equal("startadd,", sb2.ToString());

            sb = new StringBuilder("x");
            sb2 = (StringBuilder)mi.Invoke(v, new object[] { sb, "", "," });
            Assert.Equal("x", sb2.ToString());

            sb = new StringBuilder();
            sb2 = (StringBuilder)mi.Invoke(v, new object[] { sb, null, "|" });
            Assert.Equal("", sb2.ToString());
        }

        [Fact]
        public void TestPrintlnFormatsAndAppends()
        {
            var ctx = new DummyActivity();
            var v = new Mock<LogView>(ctx) { CallBase = true };
            string output = null;
            v.Setup(x => x.AppendToLog(It.IsAny<string>())).Callback<string>(s => output = s);

            v.Object.Println(Log.WARN, "tag1", "msg1", null);
            Assert.Contains("WARN", output);
            Assert.Contains("tag1", output);
            Assert.Contains("msg1", output);

            Exception ex = new Exception("Test");
            v.Object.Println(Log.ERROR, "tag2", "msg2", ex);
            Assert.Contains("ERROR", output);
            Assert.Contains("msg2", output);
            Assert.Contains("Exception", output);

            var next = new Mock<LogNode>();
            v.Object.SetNext(next.Object);
            v.Object.Println(Log.INFO, "tagx", "msgx", null);
            next.Verify(n => n.Println(It.IsAny<int>(), It.IsAny<string>(), It.IsAny<string>(), It.IsAny<Exception>()));
        }

        [Fact]
        public void TestSetAndGetNext()
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