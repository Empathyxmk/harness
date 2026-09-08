package com.trezor.mnemonic.public_tests;

import com.trezor.mnemonic.Mnemonic;
import com.trezor.mnemonic.ConfigurationError;
import org.junit.jupiter.api.*;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class PublicMnemonicTest {
    private Mnemonic mnemoEn;
    private Mnemonic mnemoFr;

    @BeforeEach
    public void setUp() {
        mnemoEn = new Mnemonic("english");
        mnemoFr = new Mnemonic("french");
    }

    @Test
    public void testPublicGenerateEntropyLengths() {
        int[] strengths = {160, 192, 224, 256};
        for (int strength : strengths) {
            String phrase = mnemoEn.generate(strength);
            assertTrue(phrase instanceof String);
            String[] words = phrase.split(" ");
            for (String w : words) {
                assertTrue(mnemoEn.getWordlist().contains(w));
            }
        }
    }

    @Test
    public void testPublicGenerateInvalidStrength() {
        int[] bads = {10, 90, 270, 512};
        for (int bad : bads) {
            assertThrows(IllegalArgumentException.class, () -> mnemoEn.generate(bad));
        }
    }

    @Test
    public void testPublicCheckValid() {
        String phrase = mnemoEn.generate(256);
        assertTrue(mnemoEn.check(phrase));
    }

    @Test
    public void testPublicCheckInvalid() {
        String phrase = "legal winner thank year wave sausage worth useful legal winner thank banana";
        assertFalse(mnemoEn.check(phrase));
    }

    @Test
    public void testPublicToMnemonicAndToEntropy() {
        String entropy = "ffffffffffffffffffffffffffffffff";
        byte[] data = hexStringToByteArray(entropy);
        String mnemonic = mnemoEn.toMnemonic(data);
        assertTrue(mnemonic instanceof String);
        byte[] recovered = mnemoEn.toEntropy(mnemonic);
        assertArrayEquals(data, recovered);
    }

    @Test
    public void testPublicFrenchWithSpace() {
        String mnemonic = mnemoFr.generate();
        assertTrue(mnemonic.contains(" "));
    }

    @Test
    public void testPublicVectors() throws IOException {
        String vectorsFile = "vectors.json";
        if (!Files.exists(Paths.get(vectorsFile))) {
            Assumptions.abort("vectors.json not available");
            return;
        }
        String json = new String(Files.readAllBytes(Paths.get(vectorsFile)));
        org.json.JSONObject j = new org.json.JSONObject(json);
        for (String lang: j.keySet()) {
            if (lang.equals("japanese")) continue;
            Mnemonic mnemo = new Mnemonic(lang);
            org.json.JSONArray arr = j.getJSONArray(lang);
            for (int i = 0; i < Math.min(2, arr.length()); ++i) {
                org.json.JSONArray v = arr.getJSONArray(i);
                String entropy = v.getString(0);
                String phrase = v.getString(1);
                assertTrue(mnemo.check(phrase), lang);
                assertArrayEquals(hexStringToByteArray(entropy), mnemo.toEntropy(phrase), lang);
            }
        }
    }

    @Test
    public void testPublicLanguageList() {
        List<String> langs = Mnemonic.listLanguages();
        assertTrue(langs.contains("italian"));
        assertTrue(langs.contains("spanish"));
    }

    @Test
    public void testPublicNormalizeString() {
        String inStr = "T\u034fesTing   Phrase";
        String out = Mnemonic.normalizeString(inStr);
        assertTrue(out.contains("esT"));
        assertTrue(out.contains("Phrase"));
    }

    @Test
    public void testPublicExpandWord() {
        String prefix = "abil";
        String expanded = mnemoEn.expandWord(prefix);
        assertTrue(expanded instanceof String);
        assertTrue(expanded.startsWith(prefix) || !expanded.equals(prefix));
    }

    @Test
    public void testPublicExpand() {
        String phrase = "abil abou above";
        String expanded = mnemoEn.expand(phrase);
        assertTrue(expanded instanceof String);
        assertTrue(expanded.contains("ability") || expanded.contains("about") || expanded.contains("above"));
    }

    // Helper
    private static byte[] hexStringToByteArray(String s) {
        int len = s.length();
        byte[] d = new byte[len / 2];
        for (int i = 0; i < len; i += 2) {
            d[i / 2] = (byte) ((Character.digit(s.charAt(i), 16) << 4)
                    + Character.digit(s.charAt(i + 1), 16));
        }
        return d;
    }
}