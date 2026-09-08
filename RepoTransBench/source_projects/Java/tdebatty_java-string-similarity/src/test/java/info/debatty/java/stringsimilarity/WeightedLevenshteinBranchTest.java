package info.debatty.java.stringsimilarity;

import org.junit.Test;
import static org.junit.Assert.*;

/**
 * Test specific branch/edge cases for WeightedLevenshtein, including custom
 * CharacterInsDelInterface/CharacterSubstitutionInterface implementations.
 */
public class WeightedLevenshteinBranchTest {

    @Test
    public void testCustomSubstitutionAndInsertionDeletion() {
        WeightedLevenshtein weighted =
                new WeightedLevenshtein(
                        new CharacterSubstitutionInterface() {
                            public double cost(char c1, char c2) {
                                // Penalty different for vowels vs others
                                if ("aeiou".indexOf(c1) >= 0 && "aeiou".indexOf(c2) >= 0) return 0.1;
                                if (c1 == c2) return 0.0;
                                return 1.0;
                            }
                        },
                        new CharacterInsDelInterface() {
                            public double insertionCost(char c) {
                                return (c == ' ') ? 0.5 : 1.0;
                            }
                            public double deletionCost(char c) {
                                return (c == '-') ? 0.2 : 1.0;
                            }
                        }
                );
        // Covers substitution, insertion, and deletion penalty branches
        assertEquals(0.1, weighted.distance("i", "e"), 0.001); // both vowels
        assertEquals(0.5, weighted.distance("abc", "ab c"), 0.001); // space insertion
        assertEquals(0.2, weighted.distance("ab-c", "abc"), 0.001); // dash deletion
        assertEquals(1.0, weighted.distance("ab", "ac"), 0.001); // default branch
    }

    @Test
    public void testZeroCostCases() {
        WeightedLevenshtein weighted = new WeightedLevenshtein(
            new CharacterSubstitutionInterface() {
                public double cost(char c1, char c2) { return (c1 == c2) ? 0.0 : 1.0; }
            }
        );
        assertEquals(0.0, weighted.distance("same", "same"), 0.0001);
    }

    @Test
    public void testNullAndEmptyCases() {
        WeightedLevenshtein weighted = new WeightedLevenshtein(
            new CharacterSubstitutionInterface() {
                public double cost(char c1, char c2) { return c1 == c2 ? 0.0 : 1.0; }
            }
        );
        assertEquals(4.0, weighted.distance("", "test"), 0.0001);
        assertEquals(2.0, weighted.distance("ab", ""), 0.0001);
        // null argument tests should throw NullPointerException
        try {
            weighted.distance(null, "abc");
            fail("Should throw NullPointerException for null input");
        } catch (NullPointerException expected) {}
    }
}