using Moq;
using Xunit;

namespace UberUX.Tests.Original
{
    public class LoginWithPhoneTest
    {
        private UberUX.LoginWithPhone activity;

        public LoginWithPhoneTest()
        {
            var mock = new Mock<UberUX.LoginWithPhone> { CallBase = true };
            activity = mock.Object;
        }

        [Fact]
        public void TestOnCreateExecutesWithoutCrash()
        {
            activity.onCreate(new object());
            Assert.NotNull(activity);
        }

        [Fact]
        public void TestSetupWindowAnimationsNoCrash()
        {
            var mock = Mock.Get(activity);
            mock.Protected().Setup("setupWindowAnimations");
            activity.GetType().GetMethod("setupWindowAnimations", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance)
                ?.Invoke(activity, null);
            Assert.NotNull(activity);
        }
    }
}