package com.itsdangerous.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.itsdangerous.exc.BadSignature;

public class ExcPublicTest {

    @Test
    public void testBadSignaturePayload() {
        BadSignature exc = new BadSignature("message", "payload");
        assertEquals("message", exc.getMessage());
        assertEquals("payload", exc.payload);
    }
}