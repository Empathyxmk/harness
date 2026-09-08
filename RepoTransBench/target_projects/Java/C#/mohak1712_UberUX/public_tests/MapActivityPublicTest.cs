using Moq;
using Xunit;

namespace UberUX.Tests.Public
{
    public class MapActivityPublicTest
    {
        private UberUX.MapActivity activity;

        public MapActivityPublicTest()
        {
            var mock = new Mock<UberUX.MapActivity> { CallBase = true };
            activity = mock.Object;
        }

        [Fact]
        public void TestOnCreateExecutesWithoutCrash_Public()
        {
            var bundle = new System.Collections.Generic.Dictionary<string, object>();
            bundle["public_test_double"] = 88.88d;
            activity.onCreate(bundle);
            Assert.NotNull(activity);
        }
    }
}