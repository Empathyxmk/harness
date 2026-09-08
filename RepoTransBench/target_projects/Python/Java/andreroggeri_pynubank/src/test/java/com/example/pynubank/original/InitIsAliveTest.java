package com.example.pynubank.original;

import com.example.pynubank.core.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class InitIsAliveTest {
    @Test
    void testIsAliveDefault() {
        HttpClient cli = new HttpClient() {
            @Override
            public DummyResponse rawGet(String url) {
                return new DummyResponse(200, url);
            }
        };
        assertTrue(cli.isAlive());
    }
}