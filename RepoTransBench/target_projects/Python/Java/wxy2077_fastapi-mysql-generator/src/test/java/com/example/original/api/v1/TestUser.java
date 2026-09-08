package com.example.original.api.v1;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class TestUser {

    static class User {
        String username, password, nickname;
        User(String u, String p, String n) { username=u; password=p; nickname=n; }
    }

    static Map<String,User> users = new HashMap<>();

    @BeforeEach
    void setup() {
        users.clear();
        users.put("alice", new User("alice", "testpass", "AliceNick"));
        users.put("bob", new User("bob", "superpass", "Bobster"));
    }

    @Test
    void testCreateUser() {
        String user = "charlie";
        String pass = "passchar";
        String nick = "Chaz";
        users.put(user, new User(user, pass, nick));
        assertTrue(users.containsKey(user), "User should exist after creation");
        assertEquals("Chaz", users.get("charlie").nickname);
    }

    @Test
    void testUserPassword() {
        assertEquals("testpass", users.get("alice").password, "Password should be testpass for alice");
        assertEquals("superpass", users.get("bob").password, "Password should be superpass for bob");
    }

    @Test
    void testNicknameChange() {
        User bob = users.get("bob");
        bob.nickname = "Bobby";
        assertEquals("Bobby", users.get("bob").nickname, "Nickname should be changed to Bobby");
    }

    @Test
    void testUserNotFound() {
        assertNull(users.get("nonexist"), "Should return null for nonexistent user");
    }
}