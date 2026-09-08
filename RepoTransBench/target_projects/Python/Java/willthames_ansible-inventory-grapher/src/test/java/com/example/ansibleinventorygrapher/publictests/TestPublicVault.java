package com.example.ansibleinventorygrapher.publictests;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

import java.io.*;
import java.nio.file.*;
import java.util.*;

class TestPublicVault {

    @Test
    void testPublicFakeVaultFile() throws IOException {
        Path tempDir = Files.createTempDirectory("testPublicFakeVaultFile");
        Path vaultFile = tempDir.resolve("public_vaultfile");
        String content = "$ANSIBLE_VAULT;1.1;AES256\ntestpublic";
        Files.writeString(vaultFile, content);

        assertTrue(Files.exists(vaultFile));

        String readContent = Files.readString(vaultFile);
        assertTrue(readContent.contains("$ANSIBLE_VAULT"));
        assertTrue(readContent.contains("public"));
    }

    @Test
    void testPublicVaultPassword() throws IOException {
        Path tempDir = Files.createTempDirectory("testPublicVaultPassword");
        Path pwFile = tempDir.resolve("public_vaultpass");
        String vaultPassword = "superpublicpw";
        Files.writeString(pwFile, vaultPassword);

        String read = Files.readString(pwFile);
        assertEquals(vaultPassword, read);
    }

    @Test
    void testPublicMultipleVaultFiles() throws IOException {
        Path tempDir = Files.createTempDirectory("testPublicMultipleVaultFiles");
        String[] vaultContents = {
            "$ANSIBLE_VAULT;1.2;AES256\npublicvaultcipher",
            "$ANSIBLE_VAULT;1.2;AES256\nanotherpubliccipher"
        };
        for (String vaultContent : vaultContents) {
            Path vaultFile = tempDir.resolve("vault_varied.public");
            Files.writeString(vaultFile, vaultContent);
            String read = Files.readString(vaultFile);
            assertTrue(read.contains("AES256"));
        }
    }
}