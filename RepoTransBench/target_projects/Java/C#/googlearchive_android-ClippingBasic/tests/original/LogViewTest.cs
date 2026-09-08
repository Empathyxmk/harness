using System;
using System.Text;
using Xunit;
using ClippingBasicSample.Log;
using Moq;

namespace ClippingBasicSample.Tests.Original
{
    public class LogViewTest
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

        public LogViewTest()
        {
            _dummyActivity = new DummyActivity();
        }

        [Fact]
        public void TestAppendIfNotNullBehavior()
        {
            var view = new LogView(_dummyActivity.RunOnUiThread);

            var sb = new StringBuilder();
            var result = view.AppendIfNotNull(sb, "abc", ",");
            Assert.Equal("abc,", result.ToString());
            sb = new StringBuilder();
            result = view.AppendIfNotNull(sb, null, "|");
            Assert.Equal("", result.ToString());

            sb = new StringBuilder("x");
            result = view.AppendIfNotNull(sb, "", "|");
            Assert.Equal("x", result.ToString());
        }

        [Fact]
        public void TestGetSetNext()
        {
            var view = new LogView(_dummyActivity.RunOnUiThread);
            var filter = new MessageOnlyLogFilter();
            view.SetNext(filter);
            Assert.Equal(filter, view.GetNext());
        }

        [Fact]
        public void TestPrintlnFormatsAndRunsRunnable()
        {
            var view = new LogView(_dummyActivity.RunOnUiThread);

            var next = new Mock<ILogNode>();
            view.SetNext(next.Object);

            var tr = new Exception("e");
            view.Println(Log.INFO, "tag", "msg", tr);

            next.Verify(m => m.Println(Log.INFO, "tag", "msg", tr), Times.Once);

            Assert.True(_dummyActivity.DidRunOnUiThread);
        }
    }
}