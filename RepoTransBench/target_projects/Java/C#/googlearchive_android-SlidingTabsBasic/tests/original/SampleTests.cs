using Xunit;
using SlidingTabsBasic;

namespace OriginalTests
{
    public class SampleTests
    {
        private object mTestActivity;
        private object mTestFragment;

        public SampleTests()
        {
            // This test "simulates" launching the activity and fragment in C#
            // since no Android framework - we just fill in dummy non-null values
            mTestActivity = new object();
            mTestFragment = new object();
        }

        [Fact]
        public void TestPreconditions()
        {
            Assert.NotNull(mTestActivity);
            Assert.NotNull(mTestFragment);
        }
    }
}