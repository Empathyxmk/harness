package com.example.pynubank.public;

import com.example.pynubank.core.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicInitIsAliveTest {
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