import org.junit.Test;

import java.util.HashSet;
import java.util.Set;

import static org.junit.Assert.*;

public class TestingSetsPublicTest {

    // Public Test: Both sets are neither empty nor null; basic set difference with no overlap
    @Test
    public void testSetDifference_noOverlap_nonNull_public() {
        Set<Integer> set1 = new HashSet<>();
        Set<Integer> set2 = new HashSet<>();
        set1.add(5);
        set2.add(7);
        Set<Integer> result = TestingSets.setDifference(new HashSet<>(set1), set2);
        assertNotNull(result);
        assertEquals(set1, result);
    }

    // Public Test: set2 is empty - set1 unchanged
    @Test
    public void testSetDifference_set2Empty_public() {
        Set<Integer> set1 = new HashSet<>();
        set1.add(9);
        Set<Integer> set2 = new HashSet<>();
        Set<Integer> result = TestingSets.setDifference(new HashSet<>(set1), set2);
        assertNotNull(result);
        assertEquals(set1, result);
    }

    // Public Test: set1 has elements, some overlap with set2
    @Test
    public void testSetDifference_withOverlap_public() {
        Set<Integer> set1 = new HashSet<>();
        set1.add(11);
        set1.add(13);
        set1.add(15);
        Set<Integer> set2 = new HashSet<>();
        set2.add(13);
        set2.add(17);
        Set<Integer> expected = new HashSet<>();
        expected.add(11);
        expected.add(15);

        Set<Integer> result = TestingSets.setDifference(new HashSet<>(set1), set2);
        assertEquals(expected, result);
    }

    // Public Test: set1 empty, set2 non-empty
    @Test
    public void testSetDifference_set1Empty_set2NonEmpty_public() {
        Set<Integer> set1 = new HashSet<>();
        Set<Integer> set2 = new HashSet<>();
        set2.add(21);
        Set<Integer> result = TestingSets.setDifference(new HashSet<>(set1), set2);
        assertNull(result);
    }

    // Public Test: set1 is null
    @Test(expected = NullPointerException.class)
    public void testSetDifference_set1Null_public() {
        Set<Integer> set2 = new HashSet<>();
        set2.add(22);
        TestingSets.setDifference(null, set2);
    }

    // Public Test: set2 is null
    @Test(expected = NullPointerException.class)
    public void testSetDifference_set2Null_public() {
        Set<Integer> set1 = new HashSet<>();
        set1.add(42);
        TestingSets.setDifference(set1, null);
    }

    // Public Test: both sets are null
    @Test(expected = NullPointerException.class)
    public void testSetDifference_bothNull_public() {
        TestingSets.setDifference(null, null);
    }

    // Public Test: set1 has elements, ALL elements in set2 (should become empty, thus return null)
    @Test
    public void testSetDifference_allElementsRemoved_public() {
        Set<Integer> set1 = new HashSet<>();
        set1.add(101); set1.add(202);
        Set<Integer> set2 = new HashSet<>();
        set2.add(202); set2.add(101); set2.add(303);
        Set<Integer> result = TestingSets.setDifference(new HashSet<>(set1), set2);
        assertNull(result);
    }

    // Public Test: set1 is empty, set2 is empty
    @Test
    public void testSetDifference_bothEmpty_public() {
        Set<Integer> set1 = new HashSet<>();
        Set<Integer> set2 = new HashSet<>();
        Set<Integer> result = TestingSets.setDifference(new HashSet<>(set1), set2);
        assertNull(result);
    }

    // Public Test: set1 and set2 identical
    @Test
    public void testSetDifference_identicalSets_public() {
        Set<Integer> set1 = new HashSet<>();
        set1.add(333); set1.add(444);
        Set<Integer> set2 = new HashSet<>();
        set2.add(444); set2.add(333);
        Set<Integer> result = TestingSets.setDifference(new HashSet<>(set1), set2);
        assertNull(result);
    }
}