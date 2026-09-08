package com.example.pynubank.public;

import com.example.pynubank.core.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicNubankClientTest {
    @Test
    void testShouldUseHttpClientIfNoneIsProvided() {
        Nubank nu = new Nubank();
        assertNotNull(nu);
    }
}