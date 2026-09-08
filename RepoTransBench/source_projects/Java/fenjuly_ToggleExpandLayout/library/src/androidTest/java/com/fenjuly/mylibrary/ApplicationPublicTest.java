package com.fenjuly.mylibrary;

import android.app.Application;
import android.test.ApplicationTestCase;

/**
 * Public version of ApplicationTest with same construction, different class name.
 */
public class ApplicationPublicTest extends ApplicationTestCase<Application> {
    public ApplicationPublicTest() {
        super(Application.class);
    }
}