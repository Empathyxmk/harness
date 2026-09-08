package com.len;

import android.app.Application;
import android.test.ApplicationTestCase;

/**
 * Public Android fundamental test with different class for demonstration.
 */
public class ApplicationPublicTest extends ApplicationTestCase<Application> {
    public ApplicationPublicTest() {
        super(Application.class);
    }
}