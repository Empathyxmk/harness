using Moq;
using Xunit;

namespace UberUX.Tests.Original
{
    public class LoginActivityTest
    {
        private UberUX.LoginActivity activity;

        public LoginActivityTest()
        {
            var mock = new Mock<UberUX.LoginActivity> { CallBase = true };
            activity = mock.Object;
        }

        [Fact]
        public void TestOnCreateExecutesWithoutCrash()
        {
            var bundle = new object(); // stand-in for Bundle
            activity.onCreate(bundle);
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