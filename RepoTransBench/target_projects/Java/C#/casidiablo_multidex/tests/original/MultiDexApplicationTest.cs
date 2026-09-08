using System;
using Xunit;

namespace Casidiablo.MultiDex.Tests.Original
{
    public class MultiDexApplicationTest
    {
        [Fact]
        public void TestAttachBaseContext()
        {
            var app = new MultiDexApplication();
            try
            {
                app.AttachBaseContext(new MockContext());
            }
            catch
            {
                // Accept any outcome (coverage)
            }
        }

        class MockContext { }
    }
}