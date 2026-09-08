package com.tiddl.public_tests;

import org.junit.jupiter.api.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class PublicConfigUnitTest {

    static class Config {
        String token = "";
        String getToken() { return token; }
        void setToken(String t) { token = t; }
        void save(Path f) throws IOException {
            Properties p = new Properties();
            p.setProperty("token", token);
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
            }
            return c;
        }
    }
    @Test
    void test_config_save_load() throws IOException {
        Path tmp = Files.createTempFile("public_unit", ".cfg");
        Config c = new Config();
        c.setToken("tok");
        c.save(tmp);
        Config c2 = Config.fromFile(tmp);
        assertEquals("tok", c2.getToken());
        Files.deleteIfExists(tmp);
    }
}