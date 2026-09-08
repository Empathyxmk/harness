using Xunit;
using RoundWidget.round;

namespace RoundWidget.Tests.Public
{
    public class RoundStatusPublicTest
    {
        [Fact]
        public void TestRadiusSettersGetters_Public()
        {
            var impl = new RoundStatusImpl();
            impl.setRadius(10f);
            impl.setTopLeftRadius(12f);
            impl.setTopRightRadius(13f);
            impl.setBottomRightRadius(14f);
            impl.setBottomLeftRadius(15f);

            Assert.Equal(10f, impl.getRadius(), 4);
            Assert.Equal(12f, impl.getTopLeftRadius(), 4);
            Assert.Equal(13f, impl.getTopRightRadius(), 4);
            Assert.Equal(14f, impl.getBottomRightRadius(), 4);
            Assert.Equal(15f, impl.getBottomLeftRadius(), 4);
        }

        [Fact]
        public void TestRadiusListLength_Public()
        {
            var impl = new RoundStatusImpl();
            float[] r = impl.getRadiusList();
            Assert.Equal(8, r.Length);
        }
    }
}