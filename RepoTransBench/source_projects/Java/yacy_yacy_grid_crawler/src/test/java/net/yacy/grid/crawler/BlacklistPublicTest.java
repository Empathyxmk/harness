package net.yacy.grid.crawler;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import net.yacy.grid.tools.MultiProtocolURL;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.regex.PatternSyntaxException;

import static org.junit.jupiter.api.Assertions.*;

public class BlacklistPublicTest {

    private Blacklist blacklist;
    private File testFile;

    @BeforeEach
    public void setUp() throws IOException {
        blacklist = new Blacklist();
        testFile = File.createTempFile("public_blacklist", ".txt");
        testFile.deleteOnExit();
    }

    @AfterEach
    public void tearDown() {
        if (testFile != null && testFile.exists()) {
            testFile.delete();
        }
    }

    @Test
    public void testLoadPlainPatterns_Public() throws IOException {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(testFile))) {
            writer.write(".*denythis.org.* # info2\n");
            writer.write("# another comment\n");
            writer.write(".*lockme.io.*\n");
        }
        blacklist.load(testFile);

        MultiProtocolURL url1 = new MultiProtocolURL("http://denythis.org/document");
        MultiProtocolURL url2 = new MultiProtocolURL("http://lockme.io/data");
        MultiProtocolURL url3 = new MultiProtocolURL("http://good.com/");
        assertNotNull(blacklist.isBlacklisted(url1.toNormalform(true), url1));
        assertNotNull(blacklist.isBlacklisted(url2.toNormalform(true), url2));
        assertNull(blacklist.isBlacklisted(url3.toNormalform(true), url3));
    }

    @Test
    public void testLoadHostPattern_Public() throws IOException {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(testFile))) {
            writer.write("host othersite.org # public host entry\n");
        }
        blacklist.load(testFile);

        MultiProtocolURL url = new MultiProtocolURL("http://othersite.org/info");
        assertNotNull(blacklist.isBlacklisted(url.toNormalform(true), url));
        MultiProtocolURL other = new MultiProtocolURL("http://diffsite.org/home");
        assertNull(blacklist.isBlacklisted(other.toNormalform(true), other));
    }

    @Test
    public void testPatternSyntaxError_Public() throws IOException {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(testFile))) {
            writer.write(".*wrong(syntax\n");
        }
        // Should log but not throw in load
        assertDoesNotThrow(() -> blacklist.load(testFile));
    }

    @Test
    public void testBlacklistInfoConstructorWithInvalidPattern_Public() {
        assertThrows(PatternSyntaxException.class, () -> new Blacklist.BlacklistInfo("*Wrong [pattern", "src2", "", null));
    }

    @Test
    public void testBlacklistCaches_Public() throws IOException {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(testFile))) {
            writer.write(".*bar.org.*\n");
        }
        blacklist.load(testFile);
        MultiProtocolURL url = new MultiProtocolURL("http://bar.org/example");
        String str = url.toNormalform(true);
        assertNotNull(blacklist.isBlacklisted(str, url));
        // Call second time to trigger cache
        assertNotNull(blacklist.isBlacklisted(str, url));
    }

    @Test
    public void testBlacklistMissCache_Public() throws IOException {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(testFile))) {
            writer.write(".*abcxyz42.com.*\n");
        }
        blacklist.load(testFile);
        MultiProtocolURL url = new MultiProtocolURL("http://notbar.org/home");
        String str = url.toNormalform(true);
        assertNull(blacklist.isBlacklisted(str, url));
        // Should be cached now
        assertNull(blacklist.isBlacklisted(str, url));
    }

    @Test
    public void testBlacklistInfoFields_Public() {
        Blacklist.BlacklistInfo bi = new Blacklist.BlacklistInfo(".*another-test.org.*", "srcFile", "extra-info", "host.org");
        assertNotNull(bi.matcher);
        assertEquals("srcFile", bi.source);
        assertEquals("extra-info", bi.info);
        assertEquals("host.org", bi.host);
    }
}