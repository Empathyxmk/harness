package com.tiddl.original;

import org.junit.jupiter.api.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class ConfigUnitTest {
    static class Config {
        String token = "";
        String user = "";
        String getToken() { return token; }
        void setToken(String t) { token = t; }
        String getUser() { return user; }
        void setUser(String u) { user = u; }
        void save(Path f) throws IOException {
            Properties p = new Properties();
            p.setProperty("token", token);
            p.setProperty("user", user);
            try (Writer w = Files.newBufferedWriter(f)) {
                p.store(w, "");
            }
        }
        static Config fromFile(Path f) throws IOException {
            Config c = new Config();
            if (Files.exists(f)) {
                Properties p = new Properties();
                try (Reader r = Files.newBufferedReader(f)) {
                    p.load(r);
                }
                c.token = p.getProperty("token", "");
                c.user = p.getProperty("user", "");
            }
            return c;
        }
    }
    @Test
    void test_config_save_load_token_and_user() throws IOException {
        Path tmp = Files.createTempFile("cfg_unit", ".cfg");
        Config c = new Config();
        c.setToken("tok2");
        c.setUser("bob");
        c.save(tmp);
        Config c2 = Config.fromFile(tmp);
        assertEquals("tok2", c2.getToken());
        assertEquals("bob", c2.getUser());
        Files.deleteIfExists(tmp);
    }
}