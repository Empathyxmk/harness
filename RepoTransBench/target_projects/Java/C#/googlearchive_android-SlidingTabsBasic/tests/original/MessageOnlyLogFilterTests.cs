using Xunit;
using Moq;
using SlidingTabsBasic.Common.Logger;
using System;

namespace OriginalTests
{
    public class MessageOnlyLogFilterTests
    {
        [Fact]
        public void TestMessageOnlyForwarded()
        {
            var next = new Mock<LogNode>();
            var filter = new MessageOnlyLogFilter(next.Object);

            filter.Println(Log.WARN, "Tag", "Message", new Exception("err"));

            next.Verify(n => n.Println(Log.NONE, null, "Message", null));
        }

        [Fact]
        public void TestNoNextDoesNothing()
        {
            var filter = new MessageOnlyLogFilter();
            filter.Println(Log.ERROR, "tag", "sample", null);
        }

        [Fact]
        public void TestSetGetNext()
        {
            var filter = new MessageOnlyLogFilter();
            Assert.Null(filter.GetNext());
            var dummy = new Mock<LogNode>();
            filter.SetNext(dummy.Object);
            Assert.Equal(dummy.Object, filter.GetNext());
        }
    }
}