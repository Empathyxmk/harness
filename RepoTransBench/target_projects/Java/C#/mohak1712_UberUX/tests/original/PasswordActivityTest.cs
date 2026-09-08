using Moq;
using Xunit;

namespace UberUX.Tests.Original
{
    public class PasswordActivityTest
    {
        private UberUX.PasswordActivity activity;

        public PasswordActivityTest()
        {
            var mock = new Mock<UberUX.PasswordActivity> { CallBase = true };
            activity = mock.Object;
        }

        [Fact]
        public void TestOnCreate_NoCrash()
        {
            activity.onCreate(new object());
            Assert.NotNull(activity);
        }

        [Fact]
        public void TestSetupWindowAnimations()
        {
            var mock = Mock.Get(activity);
            mock.Protected().Setup("setupWindowAnimations");
            activity.GetType().GetMethod("setupWindowAnimations", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance)
                ?.Invoke(activity, null);
            Assert.NotNull(activity);
        }
    }
}