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

public class BlacklistTest {

    private Blacklist blacklist;
    private File testFile;

    @BeforeEach
    public void setUp() throws IOException {
        blacklist = new Blacklist();
        testFile = File.createTempFile("blacklist", ".txt");
        testFile.deleteOnExit();
    }

    @AfterEach
    public void tearDown() {
        if (testFile != null && testFile.exists()) {
            testFile.delete();
        }
    }

    @Test
    public void testLoadPlainPatterns() throws IOException {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(testFile))) {
            writer.write(".*forbidden.com.* # info1\n");
            writer.write("# this is a comment\n");
            writer.write(".*blockme.net.*\n");
        }
        blacklist.load(testFile);

        MultiProtocolURL url1 = new MultiProtocolURL("http://forbidden.com/page");
        MultiProtocolURL url2 = new MultiProtocolURL("http://blockme.net/");
        MultiProtocolURL url3 = new MultiProtocolURL("http://allowed.com/");
        assertNotNull(blacklist.isBlacklisted(url1.toNormalform(true), url1));
        assertNotNull(blacklist.isBlacklisted(url2.toNormalform(true), url2));
        assertNull(blacklist.isBlacklisted(url3.toNormalform(true), url3));
    }

    @Test
    public void testLoadHostPattern() throws IOException {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(testFile))) {
            writer.write("host example.com # host entry\n");
        }
        blacklist.load(testFile);

        MultiProtocolURL url = new MultiProtocolURL("http://example.com/page");
        assertNotNull(blacklist.isBlacklisted(url.toNormalform(true), url));
        MultiProtocolURL other = new MultiProtocolURL("http://test.com/page");
        assertNull(blacklist.isBlacklisted(other.toNormalform(true), other));
    }

    @Test
    public void testPatternSyntaxError() throws IOException {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(testFile))) {
            writer.write(".*this[is(bad\n");
        }
        // Should log but not throw in load
        assertDoesNotThrow(() -> blacklist.load(testFile));
    }

    @Test
    public void testBlacklistInfoConstructorWithInvalidPattern() {
        assertThrows(PatternSyntaxException.class, () -> new Blacklist.BlacklistInfo("*This is [invalid", "src", "", null));
    }

    @Test
    public void testBlacklistCaches() throws IOException {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(testFile))) {
            writer.write(".*foo.com.*\n");
        }
        blacklist.load(testFile);
        MultiProtocolURL url = new MultiProtocolURL("http://foo.com/bar");
        String str = url.toNormalform(true);
        assertNotNull(blacklist.isBlacklisted(str, url));
        // Call second time to trigger cache
        assertNotNull(blacklist.isBlacklisted(str, url));
    }

    @Test
    public void testBlacklistMissCache() throws IOException {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(testFile))) {
            writer.write(".*nothingtomatch.net.*\n");
        }
        blacklist.load(testFile);
        MultiProtocolURL url = new MultiProtocolURL("http://notfoo.com/");
        String str = url.toNormalform(true);
        assertNull(blacklist.isBlacklisted(str, url));
        // Should be cached now
        assertNull(blacklist.isBlacklisted(str, url));
    }

    @Test
    public void testBlacklistInfoFields() {
        Blacklist.BlacklistInfo bi = new Blacklist.BlacklistInfo(".*test.com.*", "src", "information", "host.com");
        assertNotNull(bi.matcher);
        assertEquals("src", bi.source);
        assertEquals("information", bi.info);
        assertEquals("host.com", bi.host);
    }
}