package org.vulhub;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class AppPublicTest {

    // Utility function to match App.isCasServer implementation style: only matches lowercase "cas"
    private boolean containsCasLowerOnly(String s) {
        return s != null && s.contains("cas");
    }

    @Test
    public void testContainsCasSubstring_Public() {
        assertTrue(containsCasLowerOnly("this has cas inside"));
        assertTrue(containsCasLowerOnly("xcasY"));
        assertTrue(containsCasLowerOnly("casual"));
    }

    @Test
    public void testDoesNotContainCasSubstring_Public() {
        assertFalse(containsCasLowerOnly("CASE"));
        assertFalse(containsCasLowerOnly("archive"));
        assertFalse(containsCasLowerOnly("security"));
    }

    @Test
    public void testPerformAttack_CasPresent_Public() {
        String target = "attackcas2024";
        String expected = "Simulating CAS attack on attackcas2024";
        assertEquals(expected, App.performAttack(target));
    }

    @Test
    public void testPerformAttack_CasAbsent_Public() {
        String target = "adminpanel";
        String expected = "Target is not a CAS server: adminpanel";
        assertEquals(expected, App.performAttack(target));
    }

    @Test
    public void testPerformAttack_OnlyCasWord_Public() {
        String target = "CaS";
        // "CaS" does not contain "cas" in lowercase
        String expected = "Target is not a CAS server: CaS";
        assertEquals(expected, App.performAttack(target));
    }

    @Test
    public void testPerformAttack_CasInMiddle_Public() {
        String target = "alphaCasOmega";
        // "alphaCasOmega" does not contain "cas" in lowercase
        String expected = "Target is not a CAS server: alphaCasOmega";
        assertEquals(expected, App.performAttack(target));
    }

    @Test
    public void testPerformAttack_StartsWithCas_Public() {
        String target = "casualty";
        String expected = "Simulating CAS attack on casualty";
        assertEquals(expected, App.performAttack(target));
    }

    @Test
    public void testPerformAttack_EndsWithCas_Public() {
        String target = "smartsystems.cas";
        String expected = "Simulating CAS attack on smartsystems.cas";
        assertEquals(expected, App.performAttack(target));
    }

    @Test
    public void testPerformAttack_CasLikeButNotCAS_Public() {
        String target = "CASE";
        String expected = "Target is not a CAS server: CASE";
        assertEquals(expected, App.performAttack(target));
    }

    @Test
    public void testPerformAttack_EmptyString_Public() {
        String target = "";
        String expected = "Target is not a CAS server: ";
        assertEquals(expected, App.performAttack(target));
    }
}