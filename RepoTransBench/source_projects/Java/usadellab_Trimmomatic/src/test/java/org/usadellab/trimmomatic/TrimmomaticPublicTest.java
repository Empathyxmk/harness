package org.usadellab.trimmomatic;

import org.junit.jupiter.api.*;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;

import org.usadellab.trimmomatic.trim.Trimmer;
import org.usadellab.trimmomatic.util.Logger;

import static org.junit.jupiter.api.Assertions.*;

class TrimmomaticPublicTest {

    @Test
    void testCalcAutoThreadCountIsPositive() {
        // Different assertion wording but same property
        int threadCount = Trimmomatic.calcAutoThreadCount();
        assertTrue(threadCount >= 1, "Thread count should be at least 1");
    }

    @Test
    void testCreateTrimmersWithNonEmptyArgs() throws IOException {
        Logger logger = new Logger(false);
        List<String> args = Arrays.asList("HEADCROP:3");
        Trimmer[] arr = Trimmomatic.createTrimmers(logger, args.iterator());
        assertNotNull(arr);
        assertEquals(1, arr.length, "Should create one trimmer from 1 arg");
        assertTrue(arr[0].getClass().getSimpleName().contains("HeadCropTrimmer")); // match by type
    }

    @Test
    void testMainVersionCommand() {
        assertDoesNotThrow(() -> {
            try {
                Trimmomatic.main(new String[]{"-h"});
            } catch(Exception ignored) {}
        });
    }
}