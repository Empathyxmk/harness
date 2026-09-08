package com.example.homu.original;

import com.example.homu.auth.Auth;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class AuthTest {

    @Test
    public void testSecretHashAndCheck() {
        String secret = "top_secret";
        String encoded = Auth.secretHash(secret);
        assertTrue(encoded instanceof String);
        assertFalse(encoded.isEmpty());
        assertFalse(encoded.contains(secret));
        assertTrue(Auth.checkEncodedSecret(secret, encoded));
        assertFalse(Auth.checkEncodedSecret("wrong_secret", encoded));
    }
}