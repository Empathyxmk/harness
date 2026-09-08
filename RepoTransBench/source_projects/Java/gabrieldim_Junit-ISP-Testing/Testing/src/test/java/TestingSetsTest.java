import org.junit.Test;

import java.util.HashSet;
import java.util.Set;

import static org.junit.Assert.*;

public class TestingSetsTest {

    // Test: Both sets are neither empty nor null; basic set difference with no overlap
    @Test
    public void testSetDifference_noOverlap_nonNull() {
        Set<Integer> set1 = new HashSet<>();
        Set<Integer> set2 = new HashSet<>();
        set1.add(1);
        set2.add(2);
        Set<Integer> result = TestingSets.setDifference(new HashSet<>(set1), set2);
        assertNotNull(result);
        assertEquals(set1, result);
    }

    // Test: set2 is empty - set1 unchanged
    @Test
    public void testSetDifference_set2Empty() {
        Set<Integer> set1 = new HashSet<>();
        set1.add(3);
        Set<Integer> set2 = new HashSet<>();
        Set<Integer> result = TestingSets.setDifference(new HashSet<>(set1), set2);
        assertNotNull(result);
        assertEquals(set1, result);
    }

    // Test: set1 has elements, some overlap with set2
    @Test
    public void testSetDifference_withOverlap() {
        Set<Integer> set1 = new HashSet<>();
        set1.add(1);
        set1.add(2);
        set1.add(3);
        Set<Integer> set2 = new HashSet<>();
        set2.add(2);
        set2.add(4);
        Set<Integer> expected = new HashSet<>();
        expected.add(1);
        expected.add(3);

        Set<Integer> result = TestingSets.setDifference(new HashSet<>(set1), set2);
        assertEquals(expected, result);
    }

    // Test: set1 empty, set2 non-empty
    @Test
    public void testSetDifference_set1Empty_set2NonEmpty() {
        Set<Integer> set1 = new HashSet<>();
        Set<Integer> set2 = new HashSet<>();
        set2.add(4);
        Set<Integer> result = TestingSets.setDifference(new HashSet<>(set1), set2);
        assertNull(result);
    }

    // Test: set1 is null
    @Test(expected = NullPointerException.class)
    public void testSetDifference_set1Null() {
        Set<Integer> set2 = new HashSet<>();
        set2.add(1);
        TestingSets.setDifference(null, set2);
    }

    // Test: set2 is null
    @Test(expected = NullPointerException.class)
    public void testSetDifference_set2Null() {
        Set<Integer> set1 = new HashSet<>();
        set1.add(2);
        TestingSets.setDifference(set1, null);
    }

    // Test: both sets are null
    @Test(expected = NullPointerException.class)
    public void testSetDifference_bothNull() {
        TestingSets.setDifference(null, null);
    }

    // Test: set1 has elements, ALL elements in set2 (should become empty, thus return null)
    @Test
    public void testSetDifference_allElementsRemoved() {
        Set<Integer> set1 = new HashSet<>();
        set1.add(10); set1.add(20);
        Set<Integer> set2 = new HashSet<>();
        set2.add(10); set2.add(20); set2.add(30);
        Set<Integer> result = TestingSets.setDifference(new HashSet<>(set1), set2);
        assertNull(result);
    }

    // Test: set1 is empty, set2 is empty
    @Test
    public void testSetDifference_bothEmpty() {
        Set<Integer> set1 = new HashSet<>();
        Set<Integer> set2 = new HashSet<>();
        Set<Integer> result = TestingSets.setDifference(new HashSet<>(set1), set2);
        assertNull(result);
    }

    // Test: set1 and set2 identical
    @Test
    public void testSetDifference_identicalSets() {
        Set<Integer> set1 = new HashSet<>();
        set1.add(100); set1.add(200);
        Set<Integer> set2 = new HashSet<>();
        set2.add(100); set2.add(200);
        Set<Integer> result = TestingSets.setDifference(new HashSet<>(set1), set2);
        assertNull(result);
    }
}