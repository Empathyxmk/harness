using System;
using Xunit;
using PercentLinearLayoutLib;

namespace PercentLinearLayoutLib.Tests.Original
{
    public class PercentLinearLayoutTest
    {
        private PercentLinearLayout percentLinearLayout;

        public PercentLinearLayoutTest()
        {
            object mockContext = new object();
            object mockAttrs = new object();
            percentLinearLayout = new PercentLinearLayout(mockContext, mockAttrs);
        }

        [Fact]
        public void TestGenerateLayoutParams()
        {
            object mockAttrs = new object();
            var @params = percentLinearLayout.generateLayoutParams(mockAttrs);
            Assert.NotNull(@params);
            Assert.IsType<PercentLinearLayout.LayoutParams>(@params);
        }

        [Fact]
        public void TestLayoutParamsConstructors()
        {
            var baseParams = new LinearLayout.LayoutParams(123, 456);
            var copy1 = new PercentLinearLayout.LayoutParams(baseParams);
            Assert.Equal(123, copy1.Width);
            Assert.Equal(456, copy1.Height);

            var copy2 = new PercentLinearLayout.LayoutParams(321, 654);
            Assert.Equal(321, copy2.Width);
            Assert.Equal(654, copy2.Height);

            var marginParams = new LinearLayout.MarginLayoutParams(7, 8);
            var copy3 = new PercentLinearLayout.LayoutParams(marginParams);
            Assert.Equal(7, copy3.Width);
            Assert.Equal(8, copy3.Height);
        }
    }
}