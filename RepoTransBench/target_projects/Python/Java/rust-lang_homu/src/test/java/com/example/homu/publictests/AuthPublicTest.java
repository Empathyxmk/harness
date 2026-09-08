package com.example.homu.publictests;

import com.example.homu.auth.Auth;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class AuthPublicTest {

    @Test
    public void testSecretHashAndCheckPublic() {
        String secret = "another_secret_string";
        String encoded = Auth.secretHash(secret);
        assertTrue(encoded instanceof String);
        assertFalse(encoded.isEmpty());
        assertFalse(encoded.contains(secret));
        assertTrue(Auth.checkEncodedSecret(secret, encoded));
        assertFalse(Auth.checkEncodedSecret("wrong_public_secret", encoded));
    }
}