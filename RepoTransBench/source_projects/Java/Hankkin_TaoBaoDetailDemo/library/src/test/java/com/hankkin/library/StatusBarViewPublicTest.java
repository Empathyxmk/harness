package com.hankkin.library;

import android.content.Context;
import android.util.AttributeSet;
import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Public test for StatusBarView constructor.
 */
public class StatusBarViewPublicTest {

    public static class DummyContext extends android.test.mock.MockContext {}

    @Test
    public void testConstructorWithContext() {
        Context ctx = new DummyContext();
        StatusBarView sbv = new StatusBarView(ctx);
        assertNotNull(sbv);
    }

    @Test
    public void testConstructorWithContextAndAttrs() {
        Context ctx = new DummyContext();
        AttributeSet attrs = null;
        StatusBarView sbv = new StatusBarView(ctx, attrs);
        assertNotNull(sbv);
    }
}