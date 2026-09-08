using System;
using Xunit;
using PercentLinearLayoutLib;

namespace PercentLinearLayoutLib.PublicTests
{
    public class PercentLinearLayoutPublicTest
    {
        private PercentLinearLayout percentLinearLayout;

        public PercentLinearLayoutPublicTest()
        {
            object mockContext = new object();
            object mockAttrs = new object();
            percentLinearLayout = new PercentLinearLayout(mockContext, mockAttrs);
        }

        [Fact]
        public void TestGenerateLayoutParamsPublic()
        {
            object anotherMockAttrs = new object();
            var @params = percentLinearLayout.generateLayoutParams(anotherMockAttrs);
            Assert.NotNull(@params);
            Assert.IsType<PercentLinearLayout.LayoutParams>(@params);
        }

        [Fact]
        public void TestLayoutParamsConstructorsPublic()
        {
            var baseParams = new LinearLayout.LayoutParams(50, 75);
            var copy1 = new PercentLinearLayout.LayoutParams(baseParams);
            Assert.Equal(50, copy1.Width);
            Assert.Equal(75, copy1.Height);

            var copy2 = new PercentLinearLayout.LayoutParams(200, 125);
            Assert.Equal(200, copy2.Width);
            Assert.Equal(125, copy2.Height);

            var marginParams = new LinearLayout.MarginLayoutParams(8, 14);
            var copy3 = new PercentLinearLayout.LayoutParams(marginParams);
            Assert.Equal(8, copy3.Width);
            Assert.Equal(14, copy3.Height);
        }
    }
}