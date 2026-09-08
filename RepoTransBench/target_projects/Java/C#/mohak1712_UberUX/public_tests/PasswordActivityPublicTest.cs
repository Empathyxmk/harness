using Moq;
using Xunit;

namespace UberUX.Tests.Public
{
    public class PasswordActivityPublicTest
    {
        private UberUX.PasswordActivity activity;

        public PasswordActivityPublicTest()
        {
            var mock = new Mock<UberUX.PasswordActivity> { CallBase = true };
            activity = mock.Object;
        }

        [Fact]
        public void TestOnCreateExecutesWithoutCrash_Public()
        {
            var bundle = new System.Collections.Generic.Dictionary<string, object>();
            bundle["public_test_char"] = 'P';
            activity.onCreate(bundle);
            Assert.NotNull(activity);
        }
    }
}