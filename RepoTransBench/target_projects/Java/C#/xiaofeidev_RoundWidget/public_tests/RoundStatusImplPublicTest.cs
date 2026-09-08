using Xunit;
using RoundWidget.round;

namespace RoundWidget.Tests.Public
{
    public class RoundStatusImplPublicTest
    {
        [Fact]
        public void TestDefaultValues_Public()
        {
            var impl = new RoundStatusImpl();
            Assert.Equal(0f, impl.getRadius(), 4);
            Assert.Equal(0f, impl.getTopLeftRadius(), 4);
            Assert.Equal(0f, impl.getTopRightRadius(), 4);
            Assert.Equal(0f, impl.getBottomRightRadius(), 4);
            Assert.Equal(0f, impl.getBottomLeftRadius(), 4);
            float[] radiusList = impl.getRadiusList();
            Assert.Equal(8, radiusList.Length);
            foreach (var r in radiusList)
                Assert.Equal(0f, r, 4);
        }

        [Fact]
        public void TestSetRadius_Public()
        {
            var impl = new RoundStatusImpl();
            impl.setRadius(8.8f);
            Assert.Equal(8.8f, impl.getRadius(), 4);
            float[] radiusList = impl.getRadiusList();
            foreach (var r in radiusList)
                Assert.Equal(8.8f, r, 4);
        }

        [Fact]
        public void TestSetIndividualRadii_Public()
        {
            var impl = new RoundStatusImpl();
            impl.setRadius(2f);
            impl.setTopLeftRadius(3f);
            impl.setTopRightRadius(4f);
            impl.setBottomRightRadius(5f);
            impl.setBottomLeftRadius(6f);
            Assert.Equal(2f, impl.getRadius(), 4);
            Assert.Equal(3f, impl.getTopLeftRadius(), 4);
            Assert.Equal(4f, impl.getTopRightRadius(), 4);
            Assert.Equal(5f, impl.getBottomRightRadius(), 4);
            Assert.Equal(6f, impl.getBottomLeftRadius(), 4);

            float[] r = impl.getRadiusList();
            Assert.Equal(3f, r[0], 4);
            Assert.Equal(3f, r[1], 4);
            Assert.Equal(4f, r[2], 4);
            Assert.Equal(4f, r[3], 4);
            Assert.Equal(5f, r[4], 4);
            Assert.Equal(5f, r[5], 4);
            Assert.Equal(6f, r[6], 4);
            Assert.Equal(6f, r[7], 4);
        }

        [Fact]
        public void TestFillRadius_Public()
        {
            var impl = new RoundStatusImpl();
            impl.setRadius(2f);
            impl.setTopLeftRadius(3f);
            impl.setTopRightRadius(4f);
            impl.setBottomRightRadius(5f);
            impl.setBottomLeftRadius(6f);
            impl.setRadius(11f);
            impl.fillRadius();
            float[] list = impl.getRadiusList();
            Assert.Equal(3f, list[0], 4);
            Assert.Equal(3f, list[1], 4);
            Assert.Equal(4f, list[2], 4);
            Assert.Equal(4f, list[3], 4);
            Assert.Equal(5f, list[4], 4);
            Assert.Equal(5f, list[5], 4);
            Assert.Equal(6f, list[6], 4);
            Assert.Equal(6f, list[7], 4);
        }
    }
}