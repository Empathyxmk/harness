using Xunit;
using Moq;
using SlidingTabsBasic.Common.Logger;
using System;

namespace PublicTests
{
    public class MessageOnlyLogFilterPublicTests
    {
        [Fact]
        public void TestFiltersMessageOnlyDifferentInput()
        {
            var filter = new MessageOnlyLogFilter();
            var child = new Mock<LogNode>();
            filter.SetNext(child.Object);

            filter.Println(99, "PublicTAG", "HelloWorldMsg", null);

            child.Verify(n => n.Println(99, null, "HelloWorldMsg", null));
        }

        [Fact]
        public void TestNoNextNodeIsSafePublic()
        {
            var filter = new MessageOnlyLogFilter();
            filter.Println(88, "AnotherTAG", "SomeMessage", null);
        }

        [Fact]
        public void TestChainedNextNodePublic()
        {
            var filter = new MessageOnlyLogFilter();
            var chainChild = new Mock<LogNode>();
            filter.SetNext(chainChild.Object);

            filter.Println(5, "TagChain", "ChainedMsg", new Exception("publicChain"));
            chainChild.Verify(n => n.Println(5, null, "ChainedMsg", null));
        }
    }
}