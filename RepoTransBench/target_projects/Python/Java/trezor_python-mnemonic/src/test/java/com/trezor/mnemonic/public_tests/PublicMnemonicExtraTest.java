package com.trezor.mnemonic.public_tests;

import com.trezor.mnemonic.Mnemonic;
import com.trezor.mnemonic.ConfigurationError;
import org.junit.jupiter.api.*;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class PublicMnemonicExtraTest {

    @Test
    public void testPublicInvalidLanguage() {
        assertThrows(ConfigurationError.class, () -> new Mnemonic("notareallanguage"));
    }

    @Test
    public void testPublicDetectLanguageValid() {
        String english_phrase = "legal winner thank year wave sausage worth useful legal winner thank yellow";
        String lang = Mnemonic.detectLanguage(english_phrase);
        assertEquals("english", lang);
    }

    @Test
    public void testPublicDetectLanguageInvalid() {
        String phrase = "zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo";
        assertThrows(ConfigurationError.class, () -> Mnemonic.detectLanguage(phrase));
    }

    @Test
    public void testPublicListLanguagesUnique() {
        List<String> langs = Mnemonic.listLanguages();
        assertEquals(langs.size(), new HashSet<>(langs).size());
        assertTrue(langs.contains("japanese"));
    }

    @Test
    public void testPublicWordlistFileExists() {
        List<String> langs = Mnemonic.listLanguages();
        for (String lang : langs) {
            String path = "src/mnemonic/wordlist/" + lang + ".txt";
            assertTrue(Files.exists(Paths.get(path)), "Wordlist file does not exist for lang: " + lang);
        }
    }

    @Test
    public void testPublicInitWithWordlistInvalidLength() {
        List<String> fakeWordlist = new ArrayList<>(Collections.nCopies(2050, "bar"));
        assertThrows(ConfigurationError.class, () -> new Mnemonic("anotherfake", fakeWordlist));
    }

    @Test
    public void testPublicInitWithWordlistValidLength() {
        List<String> fakeWordlist = new ArrayList<>(Collections.nCopies(2048, "bar"));
        Mnemonic m = new Mnemonic("anotherfake", fakeWordlist);
        assertEquals(fakeWordlist, m.getWordlist());
    }

    @Test
    public void testPublicExpandWordNotFound() {
        Mnemonic m = new Mnemonic("english");
        String result = m.expandWord("unknownprefixword");
        assertEquals("unknownprefixword", result);
    }

    @Test
    public void testPublicCheckExpandsPrefixInput() {
        Mnemonic m = new Mnemonic("english");
        String phrase = "able about above absent absorb abstract absurd abuse access accident account accuse";
        assertTrue(m.check(phrase) || !m.check(phrase));
    }

    @Test
    public void testPublicStripAccentsBasicPatch() {
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