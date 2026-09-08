package me.ele.amigo.utils;

import org.junit.Test;
import static org.junit.Assert.*;

public class MessageDigestUtilPublicTest {

    @Test
    public void publicTestHashNonEmptyString() {
        String sha = MessageDigestUtil.sha1("amigo_public");
        assertNotNull(sha);
        assertNotEquals("", sha); // should not be empty for public different string
        assertTrue(sha.length() > 10);
    }

    @Test
    public void publicTestHashEmptyString() {
        String md5 = MessageDigestUtil.md5("");
        assertNotNull(md5);
        assertTrue(md5.length() > 0);
    }
}