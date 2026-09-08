package com.jude.utils;

import android.app.Activity;
import android.app.Application;
import android.os.Bundle;
import org.junit.jupiter.api.*;

import java.util.Stack;

import static org.junit.jupiter.api.Assertions.*;

class JActivityManagerTest {

    @Test
    void testStackAdditionAndRetrieval() {
        DummyActivity a1 = new DummyActivity("A1");
        DummyActivity a2 = new DummyActivity("A2");

        Stack<Activity> stack = JActivityManager.getActivityStack();
        stack.clear();

        // Try getting top activity on empty stack
        assertNull(JActivityManager.currentActivity());

        // simulate lifecycle
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
    void testCloseActivity() {
        DummyActivity a1 = new DummyActivity("A1");
        DummyActivity a2 = new DummyActivity("A2");

        Application.ActivityLifecycleCallbacks cb = JActivityManager.getActivityLifecycleCallbacks();
        cb.onActivityResumed(a1);
        cb.onActivityResumed(a2);

        JActivityManager.closeActivity(a2);
        assertEquals(a1, JActivityManager.currentActivity());

        // close null should do nothing
        JActivityManager.closeActivity(null);
        assertEquals(a1, JActivityManager.currentActivity());
    }

    @Test
    void testCloseAllActivity() {
        DummyActivity a1 = new DummyActivity("A1");
        DummyActivity a2 = new DummyActivity("A2");
        Application.ActivityLifecycleCallbacks cb = JActivityManager.getActivityLifecycleCallbacks();
        cb.onActivityResumed(a1);
        cb.onActivityResumed(a2);

        new JActivityManager().closeAllActivity();
        assertNull(JActivityManager.currentActivity());
    }

    @Test
    void testCloseActivityByName() {
        DummyActivity a1 = new DummyActivity("ActivityA");
        DummyActivity a2 = new DummyActivity("ActivityB");
        Application.ActivityLifecycleCallbacks cb = JActivityManager.getActivityLifecycleCallbacks();
        cb.onActivityResumed(a1);
        cb.onActivityResumed(a2);

        JActivityManager.closeActivityByName("com.jude.utils.ActivityB");
        assertEquals(a1, JActivityManager.currentActivity());
    }

    @Test
    void testGetCurrentActivityName() {
        DummyActivity a1 = new DummyActivity("MainScreen");
        Application.ActivityLifecycleCallbacks cb = JActivityManager.getActivityLifecycleCallbacks();
        cb.onActivityResumed(a1);

        assertEquals("com.jude.utils.MainScreen", JActivityManager.getCurrentActivityName());

        cb.onActivityDestroyed(a1);
        assertEquals("", JActivityManager.getCurrentActivityName());
    }

    @Test
    void testGetActivityStack() {
        DummyActivity a1 = new DummyActivity("AA");
        Application.ActivityLifecycleCallbacks cb = JActivityManager.getActivityLifecycleCallbacks();
        cb.onActivityResumed(a1);
        Stack<Activity> stack1 = JActivityManager.getActivityStack();
        assertFalse(stack1.isEmpty());
        Stack<Activity> stack2 = JActivityManager.getActivityStack();
        assertEquals(stack1, stack2);
    }
}