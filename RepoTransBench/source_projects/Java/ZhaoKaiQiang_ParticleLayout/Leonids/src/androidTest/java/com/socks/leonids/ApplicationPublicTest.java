package com.socks.leonids;

import android.app.Application;
import android.test.ApplicationTestCase;

// Public test: inherits ApplicationTestCase with Application.class
public class ApplicationPublicTest extends ApplicationTestCase<Application> {
    public ApplicationPublicTest() {
        super(Application.class);
    }
}