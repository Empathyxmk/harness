package com.jude.utils;

import android.app.Activity;
import android.app.Application;
import org.junit.jupiter.api.*;

import java.util.Stack;

import static org.junit.jupiter.api.Assertions.*;

class JActivityManagerPublicTest {

    @Test
    void testStackAdditionAndRetrievalPublic() {
        DummyActivity a1 = new DummyActivity("FirstActivity");
        DummyActivity a2 = new DummyActivity("SecondActivity");

        Stack<Activity> stack = JActivityManager.getActivityStack();
        stack.clear();

        assertNull(JActivityManager.currentActivity());

        Application.ActivityLifecycleCallbacks cb = JActivityManager.getActivityLifecycleCallbacks();
        cb.onActivityResumed(a1);
        assertEquals(a1, JActivityManager.currentActivity());

        cb.onActivityResumed(a2);
        assertEquals(a2, JActivityManager.currentActivity());

        cb.onActivityDestroyed(a1);
        assertEquals(a2, JActivityManager.currentActivity());

        cb.onActivityDestroyed(a2);
        assertNull(JActivityManager.currentActivity());
    }

    @Test
    void testCloseActivityPublic() {
        DummyActivity a1 = new DummyActivity("FirstActivity");
        DummyActivity a2 = new DummyActivity("SecondActivity");

        Application.ActivityLifecycleCallbacks cb = JActivityManager.getActivityLifecycleCallbacks();
        cb.onActivityResumed(a1);
        cb.onActivityResumed(a2);

        JActivityManager.closeActivity(a1);
        assertEquals(a2, JActivityManager.currentActivity());

        // Close null should still do nothing
        JActivityManager.closeActivity(null);
        assertEquals(a2, JActivityManager.currentActivity());
    }

    @Test
    void testCloseAllActivityPublic() {
        DummyActivity a1 = new DummyActivity("XActivity");
        DummyActivity a2 = new DummyActivity("YActivity");
        Application.ActivityLifecycleCallbacks cb = JActivityManager.getActivityLifecycleCallbacks();
        cb.onActivityResumed(a1);
        cb.onActivityResumed(a2);

        new JActivityManager().closeAllActivity();
        assertNull(JActivityManager.currentActivity());
    }

    @Test
    void testCloseActivityByNamePublic() {
        DummyActivity a1 = new DummyActivity("TestA");
        DummyActivity a2 = new DummyActivity("TestB");
        Application.ActivityLifecycleCallbacks cb = JActivityManager.getActivityLifecycleCallbacks();
        cb.onActivityResumed(a1);
        cb.onActivityResumed(a2);

        JActivityManager.closeActivityByName("com.jude.utils.TestA");
        assertEquals(a2, JActivityManager.currentActivity());
    }

    @Test
    void testGetCurrentActivityNamePublic() {
        DummyActivity a1 = new DummyActivity("LandingScreen");
        Application.ActivityLifecycleCallbacks cb = JActivityManager.getActivityLifecycleCallbacks();
        cb.onActivityResumed(a1);

        assertEquals("com.jude.utils.LandingScreen", JActivityManager.getCurrentActivityName());

        cb.onActivityDestroyed(a1);
        assertEquals("", JActivityManager.getCurrentActivityName());
    }

    @Test
    void testGetActivityStackPublic() {
        DummyActivity a1 = new DummyActivity("SomeActivity");
        DummyActivity a2 = new DummyActivity("AnotherActivity");
        Application.ActivityLifecycleCallbacks cb = JActivityManager.getActivityLifecycleCallbacks();
        cb.onActivityResumed(a1);
        cb.onActivityResumed(a2);

        Stack<Activity> stack1 = JActivityManager.getActivityStack();
        assertFalse(stack1.isEmpty());
        Stack<Activity> stack2 = JActivityManager.getActivityStack();
        assertEquals(stack1, stack2);
    }
}