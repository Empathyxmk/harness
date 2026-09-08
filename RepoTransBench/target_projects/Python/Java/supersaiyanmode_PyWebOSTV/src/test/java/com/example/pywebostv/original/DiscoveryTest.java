package com.example.pywebostv.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class DiscoveryTest {

    @Test
    public void testReadLocationBytesAndStr() {
        // Logic analog from Python. Implement or mock as needed.
        String msg = "LOCATION: http://somewhere/\nOther: xx";
        String result = readLocation(msg.getBytes());
        assertEquals("http://somewhere/", result);

        String msg2 = "Location: http://foo/bar\n";
        String result2 = readLocation(msg2);
        assertEquals("http://foo/bar", result2);
    }

    private String readLocation(byte[] bytes) {
        String s = new String(bytes);
        return readLocation(s);
    }

    private String readLocation(String s) {
        for (String line : s.split("\n")) {
            if (line.toLowerCase().startsWith("location:")) {
                return line.substring("location:".length()).trim();
            }
        }
        return null;
    }

    // ... implement remaining original discovery tests as appropriate.
}