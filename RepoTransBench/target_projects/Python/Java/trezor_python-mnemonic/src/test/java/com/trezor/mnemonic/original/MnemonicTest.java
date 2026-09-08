package com.trezor.mnemonic.original;

import com.trezor.mnemonic.Mnemonic;
import com.trezor.mnemonic.ConfigurationError;
import org.junit.jupiter.api.*;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class MnemonicTest {

    private Mnemonic mnemoEn;
    private Mnemonic mnemoJp;

    @BeforeEach
    public void setUp() {
        mnemoEn = new Mnemonic("english");
        mnemoJp = new Mnemonic("japanese");
    }

    @Test
    public void testGenerateEntropyLengths() {
        int[] strengths = {128, 160, 192, 224, 256};
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
    public void testGenerateInvalidStrength() {
        int[] badStr = {0, 132, 300, 1000};
        for (int bad : badStr) {
            assertThrows(IllegalArgumentException.class, () -> mnemoEn.generate(bad));
        }
    }

    @Test
    public void testCheckValid() {
        String phrase = mnemoEn.generate(128);
        assertTrue(mnemoEn.check(phrase));
    }

    @Test
    public void testCheckInvalid() {
        String phrase = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon wrong";
        assertFalse(mnemoEn.check(phrase));
    }

    @Test
    public void testToMnemonicAndToEntropy() {
        String entropy = "00000000000000000000000000000000";
        byte[] ent = hexStringToByteArray(entropy);
        String mnemonic = mnemoEn.toMnemonic(ent);
        assertTrue(mnemonic instanceof String);
        byte[] recovered = mnemoEn.toEntropy(mnemonic);
        assertArrayEquals(ent, recovered); // Stub: for all zeroes only
    }

    @Test
    public void testJapaneseNoSpace() {
        String mnemonic = mnemoJp.generate();
        assertTrue(mnemonic.contains("\u3000"));
    }

    @Test
    public void testVectors() throws IOException {
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
            for (int i = 0; i < arr.length(); ++i) {
                org.json.JSONArray v = arr.getJSONArray(i);
                String entropy = v.getString(0);
                String phrase = v.getString(1);
                assertTrue(mnemo.check(phrase), lang);
                assertArrayEquals(hexStringToByteArray(entropy), mnemo.toEntropy(phrase), lang);
            }
        }
    }

    @Test
    public void testLanguageList() {
        List<String> langs = Mnemonic.listLanguages();
        assertTrue(langs.contains("english"));
        assertTrue(langs.contains("french"));
    }

    @Test
    public void testNormalizeString() {
        String inStr = "E\u034fxample   String";
        String out = Mnemonic.normalizeString(inStr);
        assertTrue(out.contains("xample"));
        assertTrue(out.contains("String"));
    }

    @Test
    public void testExpandWord() {
        String prefix = "aban";
        String expanded = mnemoEn.expandWord(prefix);
        assertTrue(expanded instanceof String);
        assertTrue(expanded.startsWith(prefix));
    }

    @Test
    public void testExpand() {
        String phrase = "aban abou above";
        String expanded = mnemoEn.expand(phrase);
        assertTrue(expanded instanceof String);
        assertTrue(expanded.contains("abandon") || expanded.contains("about") || expanded.contains("above"));
    }

    // helper
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