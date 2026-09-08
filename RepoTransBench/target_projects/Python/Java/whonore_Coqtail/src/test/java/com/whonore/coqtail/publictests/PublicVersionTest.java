package com.whonore.coqtail.publictests;

import org.junit.jupiter.api.Test;
import com.whonore.coqtail.version.Version;
import static org.junit.jupiter.api.Assertions.*;

public class PublicVersionTest {

    @Test
    void testPublicParseVersionMinor() {
        int[] res = Version.parseVersion("Coq 8.15.0 (Feb 2022)");
        assertTrue(res instanceof int[]);
        assertEquals(8, res[0]);
        assertEquals(15, res[1]);
    }

    @Test
    void testPublicVersionCompareGreaterMajor() {
        assertTrue(Version.compareVersion(new int[] {8, 17, 0}, new int[] {8, 16, 5}) > 0);
    }

    @Test
    void testPublicVersionCompareSmallerMinor() {
        assertTrue(Version.compareVersion(new int[] {8, 7, 1}, new int[] {8, 8, 0}) < 0);
    }
}