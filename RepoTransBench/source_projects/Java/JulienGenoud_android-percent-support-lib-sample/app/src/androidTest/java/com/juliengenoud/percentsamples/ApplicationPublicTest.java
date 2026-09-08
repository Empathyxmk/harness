package com.juliengenoud.percentsamples;

import android.app.Application;
import android.test.ApplicationTestCase;

/**
 * Public test for Application class to ensure proper instantiation with a different test class name.
 */
public class ApplicationPublicTest extends ApplicationTestCase<Application> {
    public ApplicationPublicTest() {
        super(Application.class);
    }
}