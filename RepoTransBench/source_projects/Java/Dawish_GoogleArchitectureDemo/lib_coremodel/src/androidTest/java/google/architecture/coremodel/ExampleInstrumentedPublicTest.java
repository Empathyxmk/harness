package google.architecture.coremodel;

import android.content.Context;
import android.support.test.InstrumentationRegistry;
import android.support.test.runner.AndroidJUnit4;

import org.junit.Test;
import org.junit.runner.RunWith;

import static org.junit.Assert.*;

/**
 * Public Instrumented test, which will execute on an Android device, with different test value.
 */
@RunWith(AndroidJUnit4.class)
public class ExampleInstrumentedPublicTest {
    @Test
    public void useAppContext_withDifferentData() throws Exception {
        Context appContext = InstrumentationRegistry.getTargetContext();

        // Use a different (but valid-for-public-test) assertion string
        assertNotEquals("google.architecture.coremodel", appContext.getPackageName());
    }
}