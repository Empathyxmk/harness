using Xunit;
using RoundWidget.round;

namespace RoundWidget.Tests.Original
{
    public class RoundStatusImplTest
    {
        [Fact]
        public void TestDefaultValues()
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
        public void TestSetRadius()
        {
            var impl = new RoundStatusImpl();
            impl.setRadius(5.5f);
            Assert.Equal(5.5f, impl.getRadius(), 4);
            float[] radiusList = impl.getRadiusList();
            foreach (var r in radiusList)
                Assert.Equal(5.5f, r, 4);
        }

        [Fact]
        public void TestSetIndividualRadii()
        {
            var impl = new RoundStatusImpl();
            impl.setRadius(1f);
            impl.setTopLeftRadius(2f);
            impl.setTopRightRadius(3f);
            impl.setBottomRightRadius(4f);
            impl.setBottomLeftRadius(5f);
            Assert.Equal(1f, impl.getRadius(), 4);
            Assert.Equal(2f, impl.getTopLeftRadius(), 4);
            Assert.Equal(3f, impl.getTopRightRadius(), 4);
            Assert.Equal(4f, impl.getBottomRightRadius(), 4);
            Assert.Equal(5f, impl.getBottomLeftRadius(), 4);

            float[] r = impl.getRadiusList();
            Assert.Equal(2f, r[0], 4);
            Assert.Equal(2f, r[1], 4);
            Assert.Equal(3f, r[2], 4);
            Assert.Equal(3f, r[3], 4);
            Assert.Equal(4f, r[4], 4);
            Assert.Equal(4f, r[5], 4);
            Assert.Equal(5f, r[6], 4);
            Assert.Equal(5f, r[7], 4);
        }

        [Fact]
        public void TestFillRadius()
        {
            var impl = new RoundStatusImpl();
            impl.setRadius(1f);
            impl.setTopLeftRadius(2f);
            impl.setTopRightRadius(3f);
            impl.setBottomRightRadius(4f);
            impl.setBottomLeftRadius(5f);
            impl.setRadius(9f);
            impl.fillRadius();
            float[] list = impl.getRadiusList();
            Assert.Equal(2f, list[0], 4);
            Assert.Equal(2f, list[1], 4);
            Assert.Equal(3f, list[2], 4);
            Assert.Equal(3f, list[3], 4);
            Assert.Equal(4f, list[4], 4);
            Assert.Equal(4f, list[5], 4);
            Assert.Equal(5f, list[6], 4);
            Assert.Equal(5f, list[7], 4);
        }

        [Fact]
        public void TestBuilderSetsValues()
        {
            var builder = new RoundStatusImpl.RoundStatusBuilder()
                .setMRadius(1.1f)
                .setMTopLeftRadius(2.2f)
                .setMTopRightRadius(3.3f)
                .setMBottomRightRadius(4.4f)
                .setMBottomLeftRadius(5.5f);

            var impl = builder.build();
            Assert.Equal(1.1f, impl.getRadius(), 4);
            Assert.Equal(2.2f, impl.getTopLeftRadius(), 4);
            Assert.Equal(3.3f, impl.getTopRightRadius(), 4);
            Assert.Equal(4.4f, impl.getBottomRightRadius(), 4);
            Assert.Equal(5.5f, impl.getBottomLeftRadius(), 4);
        }
    }
}