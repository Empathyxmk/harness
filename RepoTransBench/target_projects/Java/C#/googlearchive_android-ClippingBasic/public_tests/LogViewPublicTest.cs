using System;
using System.Text;
using Xunit;
using Moq;
using ClippingBasicSample.Log;

namespace ClippingBasicSample.Tests.Public
{
    public class LogViewPublicTest
    {
        private class DummyActivity
        {
            public bool DidRunOnUiThread = false;
            public Action LastRunnable;
            public void RunOnUiThread(Action action)
            {
                DidRunOnUiThread = true;
                LastRunnable = action;
                action();
            }
        }

        private DummyActivity _dummyActivity;

        public LogViewPublicTest()
        {
            _dummyActivity = new DummyActivity();
        }

        [Fact]
        public void TestAppendIfNotNullPublic()
        {
            var view = new LogView(_dummyActivity.RunOnUiThread);

            var sb = new StringBuilder();
            var result = view.AppendIfNotNull(sb, "xyz", ";");
            Assert.Equal("xyz;", result.ToString());
            sb = new StringBuilder();
            result = view.AppendIfNotNull(sb, null, "~");
            Assert.Equal("", result.ToString());

            sb = new StringBuilder("y");
            result = view.AppendIfNotNull(sb, "", "?");
            Assert.Equal("y", result.ToString());
        }

        [Fact]
        public void TestGetSetNextPublic()
        {
            var view = new LogView(_dummyActivity.RunOnUiThread);
            var filter = new MessageOnlyLogFilter();
            view.SetNext(filter);
            Assert.Equal(filter, view.GetNext());
        }

        [Fact]
        public void TestPrintlnFormatsAndRunsRunnablePublic()
        {
            var view = new LogView(_dummyActivity.RunOnUiThread);

            var next = new Mock<ILogNode>();
            view.SetNext(next.Object);

            var tr = new InvalidOperationException("pubTest");
            view.Println(Log.WARN, "publicTag", "publicMsg", tr);

            next.Verify(m => m.Println(Log.WARN, "publicTag", "publicMsg", tr), Times.Once);

            // Should have executed RunOnUiThread
            Assert.True(_dummyActivity.DidRunOnUiThread);
        }
    }
}