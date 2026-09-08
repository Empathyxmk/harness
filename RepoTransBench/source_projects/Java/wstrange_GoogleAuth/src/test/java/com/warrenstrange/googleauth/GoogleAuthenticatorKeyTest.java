package com.warrenstrange.googleauth;

import org.junit.Test;

import java.lang.reflect.Constructor;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import static org.junit.Assert.*;

public class GoogleAuthenticatorKeyTest {

    /**
     * Instantiate via reflection because the constructor is non-public (private/protected/package-private).
     */
    @Test
    public void testConstructorAndGetters() throws Exception {
        GoogleAuthenticatorConfig config = new GoogleAuthenticatorConfig();
        String key = "SECRETKEY";
        int verificationCode = 123456;
        List<Integer> scratchCodes = Arrays.asList(111, 222);

        Constructor<GoogleAuthenticatorKey> constructor =
                GoogleAuthenticatorKey.class.getDeclaredConstructor(GoogleAuthenticatorConfig.class, String.class, int.class, List.class);
        constructor.setAccessible(true);

        GoogleAuthenticatorKey gak = constructor.newInstance(config, key, verificationCode, scratchCodes);

        assertEquals(key, gak.getKey());
        assertEquals(verificationCode, gak.getVerificationCode());
        assertEquals(scratchCodes, gak.getScratchCodes());
    }

    @Test
    public void testEmptyScratchCodes() throws Exception {
        GoogleAuthenticatorConfig config = new GoogleAuthenticatorConfig();
        String key = "FOO";
        int verificationCode = 0;
        List<Integer> scratchCodes = Collections.emptyList();

        Constructor<GoogleAuthenticatorKey> constructor =
                GoogleAuthenticatorKey.class.getDeclaredConstructor(GoogleAuthenticatorConfig.class, String.class, int.class, List.class);
        constructor.setAccessible(true);

        GoogleAuthenticatorKey gak = constructor.newInstance(config, key, verificationCode, scratchCodes);

        assertEquals(key, gak.getKey());
        assertEquals(verificationCode, gak.getVerificationCode());
        assertEquals(scratchCodes, gak.getScratchCodes());
    }
}