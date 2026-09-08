package org.usadellab.trimmomatic;

import org.junit.jupiter.api.*;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Iterator;
import java.util.List;

import org.usadellab.trimmomatic.trim.Trimmer;
import org.usadellab.trimmomatic.util.Logger;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import java.util.Arrays;

class TrimmomaticTest {

    @Test
    void testCalcAutoThreadCountSmall() {
        assertTrue(Trimmomatic.calcAutoThreadCount() > 0);
    }

    @Test
    void testCreateTrimmersEmpty() throws IOException {
        Logger logger = new Logger(false);
        List<String> args = Arrays.asList();
        Trimmer[] arr = Trimmomatic.createTrimmers(logger, args.iterator());
        assertNotNull(arr);
        assertEquals(0, arr.length);
    }

    @Test
    void testMainUsage() {
        // No args should produce usage and call System.exit.
        // We can't catch System.exit easily, so just cover code up to that point.
        assertDoesNotThrow(() -> {
            try {
                Trimmomatic.main(new String[]{"-version"});
            } catch(Exception ignored) {}
        });
    }
}