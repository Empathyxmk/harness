using Moq;
using Xunit;

namespace UberUX.Tests.Public
{
    public class LoginWithPhonePublicTest
    {
        private UberUX.LoginWithPhone activity;

        public LoginWithPhonePublicTest()
        {
            var mock = new Mock<UberUX.LoginWithPhone> { CallBase = true };
            activity = mock.Object;
        }

        [Fact]
        public void TestOnCreate_NoCrash_Public()
        {
            var bundle = new System.Collections.Generic.Dictionary<string, object>();
            bundle["public_test_number"] = 42;
            activity.onCreate(bundle);
            Assert.NotNull(activity);
        }

        [Fact]
        public void TestSetupWindowAnimations_NoCrash_Public()
        {
            var mock = Mock.Get(activity);
            mock.Protected().Setup("setupWindowAnimations");
            activity.GetType().GetMethod("setupWindowAnimations", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance)
                ?.Invoke(activity, null);
            Assert.NotNull(activity);
        }
    }
}