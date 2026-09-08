using Xunit;
using System.Collections.Generic;
using Jude95_Utils;

namespace Jude95_Utils.Tests
{
    public class JActivityManagerTest
    {
        [Fact]
        public void TestStackAdditionAndRetrieval()
        {
            var a1 = new DummyActivity("A1");
            var a2 = new DummyActivity("A2");

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
        public void TestCloseActivity()
        {
            var a1 = new DummyActivity("A1");
            var a2 = new DummyActivity("A2");

            var cb = JActivityManager.GetActivityLifecycleCallbacks();
            cb.OnActivityResumed(a1);
            cb.OnActivityResumed(a2);

            JActivityManager.CloseActivity(a2);
            Assert.Equal(a1, JActivityManager.CurrentActivity());

            JActivityManager.CloseActivity(null);
            Assert.Equal(a1, JActivityManager.CurrentActivity());
        }

        [Fact]
        public void TestCloseAllActivity()
        {
            var a1 = new DummyActivity("A1");
            var a2 = new DummyActivity("A2");
            var cb = JActivityManager.GetActivityLifecycleCallbacks();
            cb.OnActivityResumed(a1);
            cb.OnActivityResumed(a2);

            new JActivityManager().CloseAllActivity();
            Assert.Null(JActivityManager.CurrentActivity());
        }

        [Fact]
        public void TestCloseActivityByName()
        {
            var a1 = new DummyActivity("ActivityA");
            var a2 = new DummyActivity("ActivityB");
            var cb = JActivityManager.GetActivityLifecycleCallbacks();
            cb.OnActivityResumed(a1);
            cb.OnActivityResumed(a2);

            JActivityManager.CloseActivityByName("com.jude.utils.ActivityB");
            Assert.Equal(a1, JActivityManager.CurrentActivity());
        }

        [Fact]
        public void TestGetCurrentActivityName()
        {
            var a1 = new DummyActivity("MainScreen");
            var cb = JActivityManager.GetActivityLifecycleCallbacks();
            cb.OnActivityResumed(a1);

            Assert.Equal("com.jude.utils.MainScreen", JActivityManager.GetCurrentActivityName());

            cb.OnActivityDestroyed(a1);
            Assert.Equal("", JActivityManager.GetCurrentActivityName());
        }

        [Fact]
        public void TestGetActivityStack()
        {
            var a1 = new DummyActivity("AA");
            var cb = JActivityManager.GetActivityLifecycleCallbacks();
            cb.OnActivityResumed(a1);
            var stack1 = JActivityManager.GetActivityStack();
            Assert.False(stack1.Count == 0);
            var stack2 = JActivityManager.GetActivityStack();
            Assert.Equal(stack1, stack2);
        }
    }
}