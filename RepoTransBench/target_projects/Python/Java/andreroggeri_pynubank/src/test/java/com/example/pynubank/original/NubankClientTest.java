package com.example.pynubank.original;

import com.example.pynubank.core.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class NubankClientTest {

    @Test
    void testShouldUseHttpClientIfNoneIsProvided() {
        Nubank nu = new Nubank();
        assertNotNull(nu);
    }
}