using Xunit;
using System.Collections.Generic;
using Jude95_Utils;

namespace Jude95_Utils.PublicTests
{
    public class JActivityManagerPublicTest
    {
        [Fact]
        public void TestStackAdditionAndRetrievalPublic()
        {
            var a1 = new DummyActivity("FirstActivity");
            var a2 = new DummyActivity("SecondActivity");

            var stack = JActivityManager.GetActivityStack();
            stack.Clear();

            Assert.Null(JActivityManager.CurrentActivity());

            var cb = JActivityManager.GetActivityLifecycleCallbacks();
            cb.OnActivityResumed(a1);
            Assert.Equal(a1, JActivityManager.CurrentActivity());

            cb.OnActivityResumed(a2);
            Assert.Equal(a2, JActivityManager.CurrentActivity());

            cb.OnActivityDestroyed(a1);
            Assert.Equal(a2, JActivityManager.CurrentActivity());

            cb.OnActivityDestroyed(a2);
            Assert.Null(JActivityManager.CurrentActivity());
        }

        [Fact]
        public void TestCloseActivityPublic()
        {
            var a1 = new DummyActivity("FirstActivity");
            var a2 = new DummyActivity("SecondActivity");

            var cb = JActivityManager.GetActivityLifecycleCallbacks();
            cb.OnActivityResumed(a1);
            cb.OnActivityResumed(a2);

            JActivityManager.CloseActivity(a1);
            Assert.Equal(a2, JActivityManager.CurrentActivity());

            JActivityManager.CloseActivity(null);
            Assert.Equal(a2, JActivityManager.CurrentActivity());
        }

        [Fact]
        public void TestCloseAllActivityPublic()
        {
            var a1 = new DummyActivity("XActivity");
            var a2 = new DummyActivity("YActivity");
            var cb = JActivityManager.GetActivityLifecycleCallbacks();
            cb.OnActivityResumed(a1);
            cb.OnActivityResumed(a2);

            new JActivityManager().CloseAllActivity();
            Assert.Null(JActivityManager.CurrentActivity());
        }

        [Fact]
        public void TestCloseActivityByNamePublic()
        {
            var a1 = new DummyActivity("TestA");
            var a2 = new DummyActivity("TestB");
            var cb = JActivityManager.GetActivityLifecycleCallbacks();
            cb.OnActivityResumed(a1);
            cb.OnActivityResumed(a2);

            JActivityManager.CloseActivityByName("com.jude.utils.TestA");
            Assert.Equal(a2, JActivityManager.CurrentActivity());
        }

        [Fact]
        public void TestGetCurrentActivityNamePublic()
        {
            var a1 = new DummyActivity("LandingScreen");
            var cb = JActivityManager.GetActivityLifecycleCallbacks();
            cb.OnActivityResumed(a1);

            Assert.Equal("com.jude.utils.LandingScreen", JActivityManager.GetCurrentActivityName());

            cb.OnActivityDestroyed(a1);
            Assert.Equal("", JActivityManager.GetCurrentActivityName());
        }

        [Fact]
        public void TestGetActivityStackPublic()
        {
            var a1 = new DummyActivity("SomeActivity");
            var a2 = new DummyActivity("AnotherActivity");
            var cb = JActivityManager.GetActivityLifecycleCallbacks();
            cb.OnActivityResumed(a1);
            cb.OnActivityResumed(a2);

            var stack1 = JActivityManager.GetActivityStack();
            Assert.False(stack1.Count == 0);
            var stack2 = JActivityManager.GetActivityStack();
            Assert.Equal(stack1, stack2);
        }
    }
}