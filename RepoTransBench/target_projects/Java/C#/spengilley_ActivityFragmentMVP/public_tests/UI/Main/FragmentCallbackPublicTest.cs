using Xunit;
using ActivityFragmentMVP.UI.Main;

namespace ActivityFragmentMVP.Tests.Public.UI.Main
{
    public class FragmentCallbackPublicTest
    {
        [Fact]
        public void dummyTestForCallback()
        {
            var callback = new TestFragmentCallback();
            callback.onAction("PublicAction");
        }

        private class TestFragmentCallback : FragmentCallbackPublic
        {
            public void onAction(string s)
            {
                Assert.Equal("PublicAction", s);
            }
        }
    }
}