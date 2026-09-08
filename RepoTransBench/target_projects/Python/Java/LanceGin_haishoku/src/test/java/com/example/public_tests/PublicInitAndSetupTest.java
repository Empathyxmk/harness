package com.example.public_tests;

import org.junit.jupiter.api.Test;
import java.io.File;

import static org.junit.jupiter.api.Assertions.*;

public class PublicInitAndSetupTest {

    @Test
    public void testInitModuleExists() {
        File init = new File("src/main/java/com/example/haishoku/Init.java");
        assertTrue(init.exists());
    }

    @Test
    public void testAlgModuleExists() {
        File alg = new File("src/main/java/com/example/haishoku/alg/Alg.java");
        assertTrue(alg.exists());
    }
}