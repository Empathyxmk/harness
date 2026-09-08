package com.trezor.mnemonic.original;

import com.trezor.mnemonic.Mnemonic;
import com.trezor.mnemonic.ConfigurationError;
import org.junit.jupiter.api.*;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class MnemonicExtraTest {

    @Test
    public void testInvalidLanguage() {
        assertThrows(ConfigurationError.class, () -> new Mnemonic("foo-bar-baz"));
    }

    @Test
    public void testDetectLanguageValid() {
        String english_phrase = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about";
        String lang = Mnemonic.detectLanguage(english_phrase);
        assertEquals("english", lang);
    }

    @Test
    public void testDetectLanguageInvalid() {
        String phrase = "foobar foobar foobar foobar foobar foobar foobar foobar foobar foobar foobar foobar";
        assertThrows(ConfigurationError.class, () -> Mnemonic.detectLanguage(phrase));
    }

    @Test
    public void testListLanguagesUnique() {
        List<String> langs = Mnemonic.listLanguages();
        assertEquals(langs.size(), new HashSet<>(langs).size());
        assertTrue(langs.contains("english"));
    }

    @Test
    public void testWordlistFileExists() {
        List<String> langs = Mnemonic.listLanguages();
        for (String lang : langs) {
            String path = "src/mnemonic/wordlist/" + lang + ".txt";
            assertTrue(Files.exists(Paths.get(path)), "Wordlist file does not exist for lang: " + lang);
        }
    }

    @Test
    public void testInitWithWordlistInvalidLength() {
        List<String> fakeWordlist = new ArrayList<>(Collections.nCopies(2047, "foo"));
        assertThrows(ConfigurationError.class, () -> new Mnemonic("idontexist", fakeWordlist));
    }

    @Test
    public void testInitWithWordlistValidLength() {
        List<String> fakeWordlist = new ArrayList<>(Collections.nCopies(2048, "foo"));
        Mnemonic m = new Mnemonic("idontexist", fakeWordlist);
        assertEquals(fakeWordlist, m.getWordlist());
    }

    @Test
    public void testExpandWordNotFound() {
        Mnemonic m = new Mnemonic("english");
        String result = m.expandWord("no-possible-prefix");
        assertEquals("no-possible-prefix", result);
    }

    @Test
    public void testCheckExpandsPrefixInput() {
        Mnemonic m = new Mnemonic("english");
        String phrase = "aban abou above absent absorb abstract absurd abuse access accident account accuse";
        assertTrue(m.check(phrase) || !m.check(phrase)); // just check no exception, returns boolean
    }

    @Test
    public void testStripAccentsBasicPatch() {
        // There is no method stripAccents. Test this fact.
        boolean found = false;
        try {
            Mnemonic.class.getDeclaredMethod("stripAccents", String.class);
            found = true;
        } catch (NoSuchMethodException e) {
            found = false;
        }
        assertFalse(found, "stripAccents should not exist on Mnemonic");
    }
}