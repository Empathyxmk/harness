using Xunit;
using ActivityFragmentMVP.UI.Main;

namespace ActivityFragmentMVP.Tests.Original.UI.Main
{
    public class FragmentCallbackTest
    {
        [Fact]
        public void testInterface()
        {
            // cover the interface by implementing it
            FragmentCallback cb = new TestFragmentCallback();
            cb.loadDetailFragment();
            cb.finishProcess();
        }

        private class TestFragmentCallback : FragmentCallback
        {
            public void loadDetailFragment() { }
            public void finishProcess() { }
        }
    }
}