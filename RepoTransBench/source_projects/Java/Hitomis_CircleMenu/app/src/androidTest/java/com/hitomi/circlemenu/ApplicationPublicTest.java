package com.hitomi.circlemenu;

import android.app.Application;
import android.test.ApplicationTestCase;

/**
 * Same structure but public test: check getApplication works as expected.
 */
public class ApplicationPublicTest extends ApplicationTestCase<Application> {
    public ApplicationPublicTest() {
        super(Application.class);
    }

    public void testApplication_getsInstance() {
        Application application = getApplication();
        // In public test just assert that if created, the instance is not null (slightly different from original: performing actual assertion)
        assertNotNull(application);
    }
}