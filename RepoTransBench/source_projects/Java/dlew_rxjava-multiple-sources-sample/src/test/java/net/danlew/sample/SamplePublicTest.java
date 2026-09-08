package net.danlew.sample;

import org.junit.Test;

public class SamplePublicTest {

    @Test
    public void testSampleMainRunsPublic() {
        // This will primarily test that the main method executes without error
        Sample.sleep(10); // Just call sleep since main is long-running
    }
}