using Moq;
using Xunit;

namespace UberUX.Tests.Original
{
    public class MapActivityTest
    {
        private UberUX.MapActivity activity;

        public MapActivityTest()
        {
            var mock = new Mock<UberUX.MapActivity> { CallBase = true };
            activity = mock.Object;
        }

        [Fact]
        public void TestOnCreateExecutesWithoutCrash()
        {
            activity.onCreate(new object());
            Assert.NotNull(activity);
        }

        [Fact]
        public void TestPageTransformer_NoCrash()
        {
            var pt = activity.pageTransformer;
            Assert.NotNull(pt);
        }

        [Fact]
        public void TestPageChangeListener_NoCrash()
        {
            var plc = activity.pageChangeListener;

            plc.onPageScrollStateChanged(0);
            plc.onPageSelected(0);
            plc.onPageScrolled(0, 0.5f, 20);

            Assert.NotNull(plc);
        }
    }
}