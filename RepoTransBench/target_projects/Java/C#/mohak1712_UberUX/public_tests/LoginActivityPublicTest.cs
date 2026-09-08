using Moq;
using Xunit;

namespace UberUX.Tests.Public
{
    public class LoginActivityPublicTest
    {
        private UberUX.LoginActivity activity;

        public LoginActivityPublicTest()
        {
            var mock = new Mock<UberUX.LoginActivity> { CallBase = true };
            activity = mock.Object;
        }

        [Fact]
        public void TestOnCreateExecutesWithoutCrash_Public()
        {
            var bundle = new System.Collections.Generic.Dictionary<string, object>();
            bundle["public_test_key"] = "public_test_value";
            activity.onCreate(bundle);
            Assert.NotNull(activity);
        }

        [Fact]
        public void TestSetupWindowAnimationsNoCrash_Public()
        {
            var mock = Mock.Get(activity);
            mock.Protected().Setup("setupWindowAnimations");
            activity.GetType().GetMethod("setupWindowAnimations", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance)
                ?.Invoke(activity, null);
            Assert.NotNull(activity);
        }
    }
}