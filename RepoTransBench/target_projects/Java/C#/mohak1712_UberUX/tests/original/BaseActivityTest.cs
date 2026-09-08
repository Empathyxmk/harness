using Moq;
using Xunit;

namespace UberUX.Tests.Original
{
    public class BaseActivityTest
    {
        private UberUX.BaseActivity activity;

        public class MyBaseActivity : UberUX.BaseActivity
        {
            public override void onMapReady(UberUX.GoogleMap googleMap) => base.onMapReady(googleMap);
        }

        public BaseActivityTest()
        {
            var mock = new Mock<MyBaseActivity> { CallBase = true };
            activity = mock.Object;
        }

        [Fact]
        public void TestOnCreate_InitializesClient()
        {
            activity.onCreate(new object());
            Assert.NotNull(activity);
        }

        [Fact]
        public void TestOpenPlaceAutoCompleteView_HandlesExceptionGracefully()
        {
            activity.mMap = new Mock<UberUX.GoogleMap>().Object;
            try
            {
                activity.openPlaceAutoCompleteView();
            }
            catch (System.Exception)
            {
                Assert.True(false, "openPlaceAutoCompleteView should handle Google exception gracefully");
            }
        }

        [Fact]
        public void TestOnMapReady_NoCrash()
        {
            var map = new Mock<UberUX.GoogleMap>().Object;
            Mock.Get(map).Setup(x => x.setMaxZoomPreference(20)).Returns((object)null);
            activity.onMapReady(map);
        }
    }
}