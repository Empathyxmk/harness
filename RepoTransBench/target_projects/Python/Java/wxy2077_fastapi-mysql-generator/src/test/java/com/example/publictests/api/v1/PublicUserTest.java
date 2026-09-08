package com.example.publictests.api.v1;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class PublicUserTest {

    static class User {
        String username, password, nickname;
        User(String u, String p, String n) { username=u; password=p; nickname=n; }
    }
    static Map<String,User> users = new HashMap<>();

    @BeforeEach
    void setup() {
        users.clear();
        users.put("alice", new User("alice", "testpass", "AliceNick"));
    }

    @Test
    void testCreateUser() {
        String user = "public_bob";
        String pass = "pubpass";
        String nick = "BobPublic";
        users.put(user, new User(user, pass, nick));
        assertTrue(users.containsKey(user), "User should be created and exist in users");
    }

    @Test
    void testGetUserNickname() {
        User alice = users.get("alice");
        assertNotNull(alice, "Alice should exist");
        assertEquals("AliceNick", alice.nickname, "Should return correct nickname");
    }
}