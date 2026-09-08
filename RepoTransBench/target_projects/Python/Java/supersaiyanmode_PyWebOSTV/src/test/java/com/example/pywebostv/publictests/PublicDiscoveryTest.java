package com.example.pywebostv.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicDiscoveryTest {

    @Test
    public void testReadLocationPublic() {
        String resp = "random: entry\nLocation: http://192.168.0.101/device.xml\nAnother: entry";
        String result = readLocation(resp);
        assertEquals("http://192.168.0.101/device.xml", result);
    }

    private String readLocation(String s) {
        for (String line : s.split("\n")) {
            if (line.toLowerCase().startsWith("location:")) {
                return line.substring("location:".length()).trim();
            }
        }
        return null;
    }

    // ... Implement rest, including fake socket, monkeypatching as appropriate (could use mocks if desired)
}