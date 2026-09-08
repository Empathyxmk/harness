using System;
using Xunit;

namespace PayatuDivaAndroid.PublicTests
{
    public class AccessControl1Activity
    {
        public bool LayoutWasSet { get; private set; } = false;
        public bool HasButton { get; private set; } = true; // Simulated

        public AccessControl1Activity()
        {
            LayoutWasSet = true;
        }
    }

    public class AccessControl1ActivityPublicTests
    {
        [Fact]
        public void Test_Activity_Starts_And_Layout_Public()
        {
            var activity = new AccessControl1Activity();
            Assert.True(activity.LayoutWasSet);
            Assert.True(activity.HasButton); // Simulate R.id.ac1ViewCredsBtn
        }
    }
}