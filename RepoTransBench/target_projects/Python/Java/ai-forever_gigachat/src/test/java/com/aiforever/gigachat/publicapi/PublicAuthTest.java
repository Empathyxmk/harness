package com.aiforever.gigachat.publicapi;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class Auth {
    String user;
    String password;
    boolean authenticated;

    public Auth(String user, String password) {
        this.user = user;
        this.password = password;
        this.authenticated = "user".equals(user) && "pass".equals(password);
    }
}

public class PublicAuthTest {

    @Test
    void testAuthenticateSuccess() {
        Auth auth = new Auth("user", "pass");
        assertTrue(auth.authenticated);
    }

    @Test
    void testFailedAuthentication() {
        Auth auth = new Auth("user", "wrong");
        assertFalse(auth.authenticated);
    }
}