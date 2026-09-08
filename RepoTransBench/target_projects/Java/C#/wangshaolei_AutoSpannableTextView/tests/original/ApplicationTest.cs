using System;
using Xunit;

namespace AutoSpannableTextView.Tests.Original
{
    // This test mimics native Android ApplicationTest, adapted for C#.
    public class ApplicationTest
    {
        [Fact]
        public void ApplicationTest_BasicConstruction()
        {
            // For C#, just simulate the Application exists and can be constructed.
            var app = new FakeApplication();
            Assert.NotNull(app);
        }

        private class FakeApplication
        {
            // Empty class to simulate Android's Application
        }
    }
}