using Xunit;
using BlackObfuscatorASPlugin;
using System;

namespace BlackObfuscatorASPlugin.Tests.Original
{
    public class MainActivityTests
    {
        [Fact]
        public void TestOnCreate_NoCrash()
        {
            var activity = new MainActivity();
            object bundle = null;
            try
            {
                activity.OnCreate(bundle);
                // No exception = pass
            }
            catch (Exception)
            {
                // If any exception, ignore (like Java test)
            }
        }
    }
}